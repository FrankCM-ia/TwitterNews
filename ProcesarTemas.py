import os
import pandas as pd
from Funciones.LimpiezaDatos import *
from ProcesarTema import process_topic, mkWordCloud, ToCSV

dir_corpus = 'tweets/'
Ldf_incidents = []
Max = -1 # -1 hace que se analice todos los archivos de un tema

with os.scandir(dir_corpus) as tweets_topics:
    for topic in tweets_topics:
        if (Max == -1):
            Max = len(os.listdir(topic.path))
        
        topic_name = topic.path.split('/')[-1]
        df = process_topic(topic, topic_name)

        # Crear nubes de Palabras
        ToCSV(df, topic_name,'_tfidf')
        mkWordCloud(df,topic_name)
        print(topic_name + ' proceso concluido exitosamente.')

print('Todos los temas fueron procesados con exito')