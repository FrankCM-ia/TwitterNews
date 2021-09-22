# Librerias
from stop_words import get_stop_words
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sentiment_analysis_spanish import sentiment_analysis
from nltk.corpus import wordnet
from functions import *
from getTweets import *
from processTopic import *
from entidades import find_entities
import pandas as pd
import numpy as np
import operator

# Definir stopwords
stop_word_es = get_stop_words('spanish')
def find_top_words(data):
    # contabilizar frecuencias mediante CV
    cv = CountVectorizer(stop_words= stop_word_es)
    cv_matrix = cv.fit_transform(data['text'])
    count_words = np.sum(cv_matrix.toarray(), axis=0)
    words_cv =  {key:count_words[cv.vocabulary_[key]] for key in cv.vocabulary_}
    top_words_cv = sorted(words_cv.items(), key=operator.itemgetter(1), reverse=True)
    return top_words_cv

def get_top_entities(data):
    # preprocesar
    data_clean_for_enti = data.copy()
    data_clean_for_enti['text'] = data_clean_for_enti['text'].apply(clean_text_for_enti)

    # encontrar entidades
    entities = find_entities(data_clean_for_enti)

    # procesar entidades
    top_entities =  sorted(entities.items(), key=operator.itemgetter(1), reverse=True)[:10]

    # Encontrar significado
    dic_entities = {}
    for entity in top_entities:
        dic_entities[entity[0]] = find_mean(entity[0])
    return dic_entities    


# procesar cada trend
def for_each_trend(trend_path):
    # Leer trend - json
    trend_name = trend_path.split('\\')[-1].split('.')[0]
    data = pd.read_json(trend_path, lines=True)
    data['url'] = data['text'].apply(get_url)
    data['text'] = data['text'].apply(clean_url)
    data = data.drop_duplicates(subset=['text'])

    # Limpiar datos
    # data_clean = data['text'].apply(clean_text)

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
    return top_data_headlines_final


# ================================= MAIN =================================

categories = list(get_glossaries().keys())[:-1] + ['cusco']
topics = get_topics()
news = { i:[] for i in categories }
with os.scandir('tweets') as tweets:
    for trend in tweets:    
        trend_path = trend.path
        trend_name = trend_path.split('\\')[-1].split('.')[0]
        top_data_headlines_final = for_each_trend(trend_path)
        for _, row in top_data_headlines_final.iterrows():
            if trend_name == 'cusco':
                news['cusco'].append(create_new(row))
            else:
                news[row['tag']].append(create_new(row))
                if trend_name not in topics:
                    break

news_sorted = news.copy()
news_sorted['inicio'] = []
for new in news:
    news_sorted[new] = sorted(news[new], key = lambda dic: dic['score'], reverse = True)
    if len(news_sorted[new]) != 0:
        news_sorted['inicio'].append(news_sorted[new][0])

news_sorted['inicio'] = sorted(news_sorted['inicio'], key = lambda dic: dic['score'], reverse = True)

for cate in news_sorted:
    with open('results/'+ cate + '.json', 'w', encoding='utf-8') as file:
        dic={}
        dic['news'] = news_sorted[cate]
        json.dump(dic, file, indent=4)