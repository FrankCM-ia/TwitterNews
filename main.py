from functions import *
from CreateNews import find_headlines, create_new
from getTweets import get_topics
from WordCloud import mkWordCloud
from Entities import find_entities
from SentimenAnalysis import mkSentiment_Analysis
from stop_words import get_stop_words
import json
import os
import warnings
warnings.filterwarnings('ignore')

# Definir stopwords
stop_word_es = get_stop_words('spanish')

# Encontrar tweets relacionados a un titular
def Stem_sentence(text):
    tmp = set(clean_text(text).split()) - set(stop_word_es)
    return {stemming(word) for word in tmp}
    
def find_similarity(setA, set_pivot):
    return len(setA - set_pivot) / len(set_pivot)

def group(set_p, data, umbral = 0.5):
    data_stem =  data.copy()
    data_stem['text'] = data['text'].apply(Stem_sentence)
    data_stem['similarity'] = data_stem['text'].apply(find_similarity, set_pivot = set_p)
    data['similarity'] = data_stem['similarity']
    idx_drop = data[data['similarity'] > umbral].index
    data_final = data.drop(idx_drop)
    return data_final

# ================================= MAIN =================================

# Crear su carpeta de resultados
results = 'results/'
if not(os.path.isdir(results)):
    os.mkdir(results)
    os.mkdir(results + 'sentiment/')
    os.mkdir(results + 'wordcloud/')

categories = list(get_glossaries().keys())[:-1] + ['cusco']
topics = get_topics()
news = { i:[] for i in categories }
with os.scandir('tweets') as tweets:
    for trend in tweets:    
        trend_path = trend.path
        trend_name = trend_path.split('\\')[-1].split('.')[0]
        top_data_headlines_final, data = find_headlines(trend_path)
        top_data_headlines_final_enti = top_data_headlines_final.copy()
        top_data_headlines_final_enti['entities'] = top_data_headlines_final_enti['text'].apply(find_entities) 
        for _, row in top_data_headlines_final_enti.iterrows():
            pivot = Stem_sentence(row['text'])
            data_group = group(pivot, data)
            mkSentiment_Analysis(data_group, str(row['id']))
            mkWordCloud(data_group,str(row['id']))
            if 'cusco' in trend_name:
                news['cusco'].append(create_new(row))
            else:
                news[row['tag']].append(create_new(row))
            
news_sorted = news.copy()
news_sorted['inicio'] = []
for new in news:
    news_sorted[new] = sorted(news[new], key = lambda dic: dic['score'], reverse = True)
    if len(news_sorted[new]) != 0 and not('cusco' in new):
        news_sorted['inicio'].append(news_sorted[new][0])

news_sorted['inicio'] = sorted(news_sorted['inicio'], key = lambda dic: dic['score'], reverse = True)

for cate in news_sorted:
    with open('results/'+ cate + '.json', 'w', encoding='utf-8') as file:
        dic={}
        dic['news'] = news_sorted[cate]
        json.dump(dic, file, indent=4)