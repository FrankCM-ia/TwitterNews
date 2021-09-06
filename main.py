import os
import re
from matplotlib.pyplot import text
import pandas as pd
from functions import *
from processTopic import ToCSV, process_topic

dir_corpus = 'tweets/'
Ldf_incidents = []
Max = -1 # -1 hace que se analice todos los archivos de un tema

dic = {'id':[], 'text':[]}

with os.scandir(dir_corpus) as tweets_topics:
    for topic in tweets_topics:
        #if (Max == -1):
        #    Max = len(os.listdir(topic.path))
        
        #topic_name = topic.path.split('/')[-1]
        #df = process_topic(topic, topic_name)

        # Crear nubes de Palabras
        #ToCSV(df, topic_name,'_tfidf')
        #mkWordCloud(df,topic_name)
        #print(topic_name + ' proceso concluido exitosamente.')

        df = pd.read_csv(topic.path, sep=';')
        texto = list(df['text'])
        id = list(df['Unnamed: 0'])

        #dir = re.sub('.csv', "", topic.path)

        for i in range(0,len(id)):
            dic['id'].append(id[i])
            dic['text'].append(texto[i])
        
    df = pd.DataFrame(dic)
    ToCSV(df,'Willax','')


print('Todos los temas fueron procesados con exito')


