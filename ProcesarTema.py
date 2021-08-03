from operator import index
import os
import re
import json
import pandas as pd
from nltk import tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from Funciones.LimpiezaDatos import *
from Funciones.TokenizarDatos import *
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')

# ================================= LIMPIEZA DE DATOS =================================
def df_data(file_csv):
  df = pd.read_csv(file_csv, sep=';')
  columns = list(df["Unnamed: 0"])
  df = df.drop(["Unnamed: 0"], axis = 1)
  dic = {k:v for k,v in enumerate(columns)}
  df.rename(index=dic, inplace=True)

  for i in df.index:
    text = str(df.loc[i].text)
    new_text = spr_emoji(text)
    new_text = new_text.lower() 
    new_text = re.sub('http\S+', ' ', new_text)
    new_text = spr_punctuation(new_text)
    #new_text = re.sub("\d+", ' ', new_text)
    new_text = re.sub("\\s+", ' ', new_text)
    df.loc[i] = new_text
  return df

# ================================= TOKENIZAR DATOS =================================
def Tokenize(func, text):
    tokens = nltk.word_tokenize(text)
    tokens = [token for token in tokens if len(token) > 2]
    tokens = [func(token) for token in tokens]
    return tokens

def Tokenize_Stem(text):
    return Tokenize(stemming, text)

def Tokenize_Lemma(text):
    return Tokenize(lemmatize, text)

# ================================= ANALISIS DE DATOS =================================
def mkWordCloud(df_tf_idf, topic):
    name = re.sub('.csv', "", topic)
    name = 'Graficas/' + name + '/' + name + '.png'
    Cloud = WordCloud(background_color="white", max_words=50).generate_from_frequencies(df_tf_idf.T.sum(axis=1))
    Cloud.to_file(name) #Guardamos la imagen generada
    plt.axis('off')
    print("Nube " +  name + '.png' + " Creada")

def ToCSV(dataframe, topic, type):
    name = re.sub('.csv', "", topic)
    addr ='Graficas/' + name + '/'+ name + type + '.csv'
    dataframe.to_csv(addr, sep=';', encoding = 'utf-8') 
    

# ====================================================================================
# ********************************* FUNCION PRICIPAL *********************************
# ====================================================================================
def process_topic(dir_addr, topic_name, func = Tokenize_Lemma):
    df_tweets = df_data(dir_addr)
    ToCSV(df_tweets, topic_name, '')
    
    StopWords = list(stopwords.words('spanish'))
    topic_name = 'rt ' + spr_punctuation(topic_name.lower()) #+ ' ' + lemmatize(topic_name.lower())
    topic_name = topic_name.split(' ')
    StopWords.extend((topic_name))
    TF_IDF = TfidfVectorizer(stop_words = StopWords, tokenizer = func)

    corpus = list(df_tweets['text'])
    ids = df_tweets.index

    vecs = TF_IDF.fit_transform(corpus)
    feature_names = TF_IDF.get_feature_names()
    #print(feature_names)
    dense = vecs.todense()
    lst = dense.tolist()
    df = pd.DataFrame(lst, columns=feature_names, index=ids)
    return df
    

# ------------------------ EJEMPLO COMO PROCESAR UN TEMA ------------------------
topic = 'Malmo.csv'
dir_addr = 'tweets/' + topic

#df  = df_data(dir_addr)
#ToCSV(df, topic)
# df_tf_idf = process_topic(dir_addr, topic)
# ToCSV(df_tf_idf, topic, '_tfidf')
# mkWordCloud(df_tf_idf, topic)
