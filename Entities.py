from functions import *
import nltk
import nltk.stem
import spacy
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
import stanza
import warnings
warnings.filterwarnings('ignore')

# INSTALANDO DEPENDENCIAS PARA PODER OPERAR CON EL LENGUAJE ESPAÑOL
stanza.download('es', package='ancora', processors='tokenize,mwt,pos,lemma', verbose=True)
stNLP = stanza.Pipeline(processors='tokenize,mwt,pos,lemma', lang='es', use_gpu=True)

#descarga de paquete de palabras para omitir
stopwords.words('spanish')

#========= MODULOS =================
nlp=spacy.load('es_core_news_lg')

def find_entities(text):
    text = clean_text_for_enti(text)
    Entidades={}
    doc = nlp(text)
    for token in doc.ents:
        if(token.label_== "ORG" or token.label_== "PER" or token.label_== "LOC" or token.label_== "MISC"):
            if token.lemma_ in Entidades:
                Entidades[token.lemma_] += 1
            else:
                Entidades[token.lemma_] = 1
    for i in doc:
        if(i.pos_== "PROPN" or i.pos_== "NOUN"):
            if i in Entidades:
                Entidades[str(i)] += 1
            else:
                Entidades[str(i)] = 1

    enti = { i for i in set(Entidades.keys()) if len(i) > 2 and len(i.split()) < 5}
    return list(enti)

# def get_top_entities(data):
#     # preprocesar
#     data_clean_for_enti = data.copy()
#     data_clean_for_enti['text'] = data_clean_for_enti['text'].apply(clean_text_for_enti)

#     # encontrar entidades
#     entities = find_entities(data_clean_for_enti)

#     # procesar entidades
#     top_entities =  sorted(entities.items(), key=operator.itemgetter(1), reverse=True)[:10]

#     # Encontrar significado
#     dic_entities = {}
#     for entity in top_entities:
#         dic_entities[entity[0]] = find_mean(entity[0])
#     return dic_entities    

