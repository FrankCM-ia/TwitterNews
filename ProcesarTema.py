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
from Funciones.AnalisisDatos import *
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')

# ================================= LIMPIEZA DE DATOS =================================
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
def process_topic(dir_addr, topic_name, Max , func = Tokenize_Lemma):
    StopWords = list(stopwords.words('spanish'))
    topic_name = 'rt ' + spr_punctuation(topic_name.lower()) #+ ' ' + lemmatize(topic_name.lower())
    topic_name = topic_name.split(' ')
    StopWords.extend((topic_name))
    print(StopWords)
    TF_IDF = TfidfVectorizer(stop_words = StopWords, tokenizer = func)

    df_tweets = df_data(dir_addr, Max)
    corpus = list(df_tweets['Texto'])

    vecs = TF_IDF.fit_transform(corpus)
    feature_names = TF_IDF.get_feature_names()
    #print(feature_names)
    dense = vecs.todense()
    lst = dense.tolist()
    df = pd.DataFrame(lst, columns=feature_names)
    return df
    

# ------------------------ EJEMPLO COMO PROCESAR UN TEMA ------------------------
topic = '#BetoASaber'
dir_addr = 'tweets/' + topic

Max = 2000
df_tf_idf = process_topic(dir_addr, topic, Max)
#ToCSV(df_tf_idf, topic, name=topic+'_tf_idf')
mkWordCloud(df_tf_idf, str(Max) + "t_" + topic + '_Lemma', topic)
