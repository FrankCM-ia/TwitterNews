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

    # contabilizar frecuencia mediante IDF
    tfidf = TfidfTransformer()
    tfidf_matrix = tfidf.fit_transform(cv_matrix)
    words_idf =  dict(zip(cv.get_feature_names(), tfidf.idf_))
    top_words_idf =  sorted(words_idf.items(), key=operator.itemgetter(1), reverse=True)
    return top_words_cv, top_words_idf

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


# Leer glosarios y crear outputs
glossaries = {}
with os.scandir('glossaries') as gloss_scanIte:
    for txt in gloss_scanIte:
        tmp = open(txt, 'r').readlines()
        lines = [ without_accents(word.rsplit('\n')[0]) for word in tmp]
        name = txt.path.split('\\')[-1].split('.')[0]
        glossaries[name] = lines

        # crear archivo output
        file = open('results/' + name + '.json', 'a')
        file.close()

# procesar cada trend
def for_each_trend(trend_path):
    # Leer trend - json
    data = pd.read_json(trend_path, lines=True)
    trend_name = trend_path.split('\\')[-1].split('.')[0]

    # Limpiar datos
    data_clean = clean_data(trend_path)

    # Top palabras mas usadas
    cv, _ = find_top_words(data_clean)

    # Identificar categoria del trend 
    points = {}
    for key in glossaries:
        count = 0
        tmp = []
        for word, score in cv:
            if word in glossaries[key]:
                tmp.append(word)
                count += score
        points[key] = count
    category = sorted(points.items(), key=operator.itemgetter(1), reverse=True)[0][0]
    score = sorted(points.items(), key=operator.itemgetter(1), reverse=True)[0][1]

    # Identificar titular
    data_score = data.copy()
    data_score['score'] = data_score['user_followers'] * data_score['retweet_count'] * data_score['favorite_count']
    data_score_top_by_score = data_score.sort_values('score', ascending=False)

    # entidades y significados
    dic_entities =  get_top_entities(data)

    # Noticia
    new = {}
    new['title'] = str(data_score_top_by_score.iloc[0,1])
    new['date'] = str(data_score_top_by_score.iloc[0,6])
    new['img'] = str(data_score_top_by_score.iloc[0,8])
    new['category'] = str(category)
    new['score'] =  int(score)
    new['entities'] = dic_entities
    print('[✓] New about '+ trend_name + ' created.')
    return new, str(category)

#for_each_trend('tweets\#BTSxWeAreUnderTheSameMoon.json')
dic_category = {}
with os.scandir('tweets') as tweets:
    for trend in tweets:
        new, category =  for_each_trend(trend.path)
        if category in set(dic_category.keys()):
            dic_category[category].append(new)
        else:
            dic_category[category] = [new]

for cate in dic_category:
    with open('results/'+ cate + '.json', 'a', encoding='utf-8') as file:
        dic={}
        dic['news'] = dic_category[cate]
        json.dump(dic, file, indent=4)