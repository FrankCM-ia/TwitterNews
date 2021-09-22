from functions import *
import pandas as pd
import operator

def find_top_group(data):
    data_top_by_favorite = data.sort_values('favorite_count', ascending=False)
    top_tweets_by_favorite = { k:2 for k in data_top_by_favorite['id'].head(10)}

    data_top_by_user_followers = data.sort_values('user_followers', ascending=False)
    top_tweets_by_user_followers = { k:3 for k in data_top_by_user_followers['id'].head(10)} 

    data_top_by_retweet_count = data.sort_values('retweet_count', ascending=False)
    top_tweets_by_retweet_count = { k:1 for k in data_top_by_retweet_count['id'].head(10)}

    data_score = data.copy()
    data_score['score'] = data_score['user_followers'] * data_score['retweet_count'] * data_score['favorite_count']
    top_tweets_by_score = { k:4 for k in data_score['id'].head(10)}

    ids = set(top_tweets_by_favorite.keys()) | set(top_tweets_by_user_followers.keys()) | set(top_tweets_by_retweet_count.keys()) | set(top_tweets_by_score.keys())
    headlines = {}
    for id in ids:
        fa = get_value(top_tweets_by_favorite, id)
        uf = get_value(top_tweets_by_user_followers, id)
        rc = get_value(top_tweets_by_retweet_count, id)
        sc = get_value(top_tweets_by_score, id)
        headlines[id] = fa + uf + rc + sc
    top_headlines = sorted(headlines.items(), key = operator.itemgetter(1), reverse=True)[:10]
    top_headlines_dic = { i[0]:i[1]  for i in top_headlines}

    data_headlines =  data[data.id.isin(list(top_headlines_dic.keys()))]
    data_headlines['score'] = [ top_headlines_dic[id] for id in data_headlines['id']]
    top_data_headlines = data_headlines.sort_values('score', ascending=False)
    return top_data_headlines

def tag_news(text):
    glossaries = get_glossaries()
    point = 0
    tag = 'otros'
    for key in glossaries:
      if key != 'zbad':
        c = eval_top_words(text, glossaries[key])
        if c > point:
          point = c
          tag = key
      else:
        c = eval_top_words(text, glossaries[key])
        point = point - c
    if point <= 0: tag = 'otros'
    return tag + ' ' + str(point)

# Encontrar titulares para trend
def find_headlines(trend_path):
    # Leer trend - json
    trend_name = trend_path.split('\\')[-1].split('.')[0]
    data = pd.read_json(trend_path, lines=True)
    data['url'] = data['text'].apply(get_url)
    data['text'] = data['text'].apply(clean_url)
    data = data.drop_duplicates(subset=['text'])

    # Encontrar grupo de potenciales titulares
    top_data_headlines = find_top_group(data)

    # Taggear e identificar titular 
    top_data_headlines['tag'] = top_data_headlines['text'].apply(tag_news) 
    top_data_headlines['tag_point'] = top_data_headlines['tag'].apply(lambda text: int(text.split()[1]))
    top_data_headlines['tag'] = top_data_headlines['tag'].apply(lambda text: text.split()[0]) 
    top_data_headlines['sum_p'] = top_data_headlines['score'] + top_data_headlines['tag_point']
    idx_drop = top_data_headlines[top_data_headlines['tag'] == 'otros'].index
    top_data_headlines_final = top_data_headlines.drop(idx_drop)
    top_data_headlines_final = top_data_headlines_final.drop_duplicates(subset=['text'])
    top_data_headlines_final = top_data_headlines_final.sort_values('sum_p', ascending=False)
    print('[✓] ' + trend_name + ' news found successfully.')
    return top_data_headlines_final, data

# Noticia
def create_new(row_data_news):
    new = {}
    new['id'] = row_data_news['id']
    new['title'] = row_data_news['text']
    new['date'] = str(row_data_news['date'])
    new['screen_name'] = row_data_news['screen_name']
    new['name'] = row_data_news['name']
    new['img'] = row_data_news['img']
    new['url'] = row_data_news['url']
    new['category'] = row_data_news['tag']
    new['score'] = row_data_news['sum_p']
    new['sentiment'] = 'sentiment/'  + str(row_data_news['id']) + '.jpg'
    new['wordcloud'] = 'wordcloud/'  + str(row_data_news['id']) + '.jpg'
    new['entities'] = row_data_news['entities']
    return new