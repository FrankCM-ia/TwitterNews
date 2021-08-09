from operator import add
import re
import nltk
import pandas as pd
import seaborn as sns
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from matplotlib import style
from wordcloud import WordCloud
from Funciones.LimpiezaDatos import *
from Funciones.TokenizarDatos import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import warnings
warnings.filterwarnings('ignore')


#%matplotlib inline  
style.use('fivethirtyeight')
sns.set(style='whitegrid',color_codes=True)

# ================================= LIMPIEZA DE DATOS =================================
def df_data(file_csv):
  df = pd.read_csv(file_csv, sep=';')
  columns = list(df["Unnamed: 0"])
  df = df.drop(["Unnamed: 0"], axis = 1)
  dic = {k:v for k,v in enumerate(columns)}
  df.rename(index=dic, inplace=True)

  df['text'] = df['text'].apply(func = clean_text)
  # "NOUN","ADJ","ADV","PROPN","NUM", "VERB"
  df['text'] = df['text'].apply(func = Tagging, Tipos = ["NOUN","ADJ","ADV"])  
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
    name = re.sub('.csv', "", topic_name)
    #ToCSV(df_tweets, topic_name, '') 

    StopWords = list(stopwords.words('spanish'))
    topic_name = 'rt ' + PO + spr_punctuation(topic_name.lower()) #+ ' ' + lemmatize(topic_name.lower())
    topic_name = topic_name.split(' ')
    StopWords.extend((topic_name))

    TF_IDF = TfidfVectorizer(stop_words = StopWords, tokenizer = func)
    text_vec = TF_IDF.fit_transform(df_tweets['text'])

    lda_model=LatentDirichletAllocation(n_components = 4 ,learning_method='online',random_state=42,max_iter=75)
    lda_top=lda_model.fit_transform(text_vec)
    vocab = TF_IDF.get_feature_names()

    for i in range(0,len(lda_model.components_)):
        imp_words_topic=""
        comp = lda_model.components_[i]
        vocab_comp = zip(vocab, comp)
        sorted_words = sorted(vocab_comp, key= lambda x:x[1], reverse=True)[:50]
        for word in sorted_words:
            imp_words_topic=imp_words_topic+" "+word[0]
            
        addr ='Graficas/' + name + '/'+ name + 'subtopic' + str(i) + '.png'
        wordcloud = WordCloud(width=600, height=400).generate(imp_words_topic)
        wordcloud.to_file(addr)

# ------------------------ EJEMPLO COMO PROCESAR UN TEMA ------------------------
topic = '#CierrenWillax.csv'
dir_addr = 'tweets/' + topic

# df  = df_data(dir_addr)
# ToCSV(df,topic,'')
process_topic(dir_addr, topic)
#ToCSV(df_tf_idf, topic, '_tfidf')
#mkWordCloud(df_tf_idf, topic)
