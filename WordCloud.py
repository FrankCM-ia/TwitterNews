from IPython.display import display
from functions import *
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud, ImageColorGenerator
from stop_words import get_stop_words
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
stop_word_es = get_stop_words('spanish')
Adicionales=['si','es','ser','mas','ahora','todavia','asi','pm','ahi']
stop_word_es.extend(Adicionales)

# Creamos el BOW del corpus 
def mkWordCloud(data,trendName):
    corpus = data['text'].apply(clean_text)
    NombreNube = trendName + '.jpg'

    #utilizo la funcion CountVectorizer para  vectorizar las palabras en una matriz
    bow_corpus = CountVectorizer(stop_words = stop_word_es).fit(corpus)
    #Recolectamos los nombre
    count_tokens=bow_corpus.get_feature_names()
    corpus_vect = bow_corpus.transform(corpus)

    #Creamos nuestro diccionario
    count_words = np.asarray(corpus_vect.sum(axis=0))[0]
    diccionario = {count_tokens[n]: count_words[n] for n in range(len(count_tokens))}
   
    # Mostramos la nube de palabras
    wordcloud = WordCloud(width=600,height=400, background_color='white',colormap='Dark2')#, max_words=70)#mask=peru_mask
    wordcloud.generate_from_frequencies(frequencies=diccionario)
    wordcloud.to_file('results/wordcloud/'+NombreNube)

