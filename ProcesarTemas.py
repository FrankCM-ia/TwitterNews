from Funciones.AnalisisDatos import ToCSV
import os
from ProcesarTema import process_topic2, mkWordCloud

dir_corpus = 'tweets/'
Ldf_incidents = []
Max = 100
with os.scandir(dir_corpus) as tweets_topics:
    for topic in tweets_topics:
        topic_name = topic.path.split('/')[-1]
        df1 = process_topic2(topic, topic_name.lower(), Max)
        df2 = process_topic2(topic, topic_name.lower(), Max,  stem=True)

        # Crear nubes de Palabras
        mkWordCloud(df1, str(Max) + "t_" + topic_name + '_Lemma', topic_name)
        mkWordCloud(df2, str(Max) + "t_" + topic_name + '_Stem_', topic_name)

print('exito')