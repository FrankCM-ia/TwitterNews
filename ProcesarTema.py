import os
import re
import json
import pandas as pd
from nltk import tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from Funciones.LimpiezaDatos import *
from Funciones.ReduccionComplejidad import *
from Funciones.AnalisisDatos import *
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')

# ================================= LIMPIEZA DE DATOS =================================
def clean_data(topic_addr):
    cl_data = {}
    with os.scandir(topic_addr) as tweets_dir:
        for tweet in tweets_dir:
            with open(tweet.path) as tweet_js:
                tweet = json.load(tweet_js)
                id = tweet["id_str"]
                full_text = tweet["full_text"]
                full_text = spr_emoji(full_text)
                full_text = spr_punctuation(full_text)
                full_text = re.sub("\d+", ' ', full_text)
                full_text = full_text.lower()
                cl_data[id] = nltk.word_tokenize(full_text)
                cl_data[id] = spr_link(cl_data[id])
    return cl_data


def df_data(topic_addr, Max):
    cl_data = []
    with os.scandir(topic_addr) as tweets_dir:
        c = 0
        for tweet in tweets_dir:
            if (c == Max):
                break
            tmp = []
            with open(tweet.path) as tweet_js:
                tweet = json.load(tweet_js)
                full_text = tweet["full_text"]
                new_text = spr_emoji(full_text)
                new_text = new_text.lower()
                new_text = re.sub('http\S+', ' ', new_text)
                new_text = spr_punctuation(new_text)
                new_text = re.sub("\d+", ' ', new_text)
                new_text = re.sub("\\s+", ' ', new_text)
                tmp.append(new_text)
            cl_data.append(tmp)
            c += 1
    df = pd.DataFrame(cl_data, columns=['Texto'])
    return df

def Tokenize_Lemma(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token for token in tokens if len(token) > 2]
    tokens = [lemmatize(token) for token in tokens]
    return tokens

def Tokenize_Stem(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token for token in tokens if len(token) > 2]
    tokens = [stemming(token) for token in tokens]
    return tokens

# ================================= REDUCCION DE COMPLEJIDAD =================================
def process_corpus(tokens_tweets_dic):
    for id in tokens_tweets_dic:
        tokens_tweets_dic[id] = spr_StopWords(tokens_tweets_dic[id])
        tokens_tweets_dic[id] = lemmatize_Tokens(tokens_tweets_dic[id])
    return tokens_tweets_dic

def mkBOW(tokens_tweets_dic):
    dic_tokens_CP = process_corpus(tokens_tweets_dic)
    bow = []
    for id in tokens_tweets_dic:
        bow = bow + dic_tokens_CP[id]
        bow = unique(bow)
    return bow

# ================================= ANALISIS DE DATOS =================================
def mkDataFrame(bow, tokens_tweets_dic):
    bow = mkBOW(tokens_tweets_dic)

    # Poner el BOW en un dicionario de list vacias
    incidents_bow_dic = {}
    for word in bow:
        incidents_bow_dic[word] = []

    # Contar incidencias 
    for id in tokens_tweets_dic:
        incidents_bow_dic = count_incidents(incidents_bow_dic, tokens_tweets_dic[id])

    # Selecionar datos para el Data Frame
    ids = tokens_tweets_dic.keys()
    easy_ids = [i+1 for i in range(0,len(ids))]
    df = pd.DataFrame(incidents_bow_dic, index = easy_ids)
    return df

def mkWordCloud(df_tf_idf, name, topic):
    name = 'Graficas/' + topic + '/' + name + '.png'
    Cloud = WordCloud(background_color="white", max_words=50).generate_from_frequencies(df_tf_idf.T.sum(axis=1))
    Cloud.to_file(name) #Guardamos la imagen generada
    plt.axis('off')
    print("Nube " +  name + '.png' + " Creada")

def term_frequency_analysi(dataframe):
    df_step_tf = tf(dataframe)
    df_step_idf = idf(df_step_tf)
    df_step_tf_idf = tf_idf(df_step_tf, df_step_idf)
    return df_step_tf_idf


# ====================================================================================
# ********************************* FUNCION PRICIPAL *********************************
# ====================================================================================
# ------------------------ Funciones ------------------------
def process_topic1(dir_addr):
    dic_tokens_tweets = clean_data(dir_addr)
    bow = mkBOW(dic_tokens_tweets)
    df_incidents_bow = mkDataFrame(bow, dic_tokens_tweets)
    return df_incidents_bow

def process_topic2(dir_addr, topic_name, Max ,stem = False, ):
    stop_words = list(stopwords.words('spanish'))
    stop_words.extend(("rt",""))
    topic_name = topic_name.split(' ')
    stop_words.extend((topic_name))

    TF_IDF_LEMMA = TfidfVectorizer(stop_words=stop_words, tokenizer=Tokenize_Lemma)
    TF_IDF_STEM = TfidfVectorizer(stop_words=stop_words, tokenizer=Tokenize_Stem)

    df_tweets = df_data(dir_addr, Max)
    corpus = list(df_tweets['Texto'])

    TF_IDF = TF_IDF_LEMMA
    if stem:
        TF_IDF = TF_IDF_STEM

    vecs = TF_IDF.fit_transform(corpus)
    feature_names = TF_IDF.get_feature_names()
    dense = vecs.todense()
    lst = dense.tolist()
    df = pd.DataFrame(lst, columns=feature_names)
    return df
    

# ------------------------ COMO PROCESAR UN TEMA ------------------------
##topic = 'Estados Unidos'
#dir_addr = 'tweets/' + topic
#df = process_topic1(dir_addr)
#df_tf = tf(df)
#ToCSV(df_tf, topic, name=topic+'_tf')

#Max = 300
#df_tf_idf = process_topic2(dir_addr, topic.lower(), Max)
#ToCSV(df_tf_idf, topic, name=topic+'_tf_idf')
#print(df_tf_idf)
#mkWordCloud(df_tf_idf, str(Max) + "t_" + topic + '_Lemma', topic)

#df2 = process_topic2(dir_addr, stem=True)
#ToCSV(df1)
# Crear la nube
# mkWordCloud(df1, topic + '_Lemma_60', topic)

# mkWordCloud(df2, topic + '_Stem_60', topic)
# hola