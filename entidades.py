import pandas as pd
import nltk
import nltk.stem
import spacy
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
import stanza

# INSTALANDO DEPENDENCIAS PARA PODER OPERAR CON EL LENGUAJE ESPAÑOL
stanza.download('es', package='ancora', processors='tokenize,mwt,pos,lemma', verbose=True)
stNLP = stanza.Pipeline(processors='tokenize,mwt,pos,lemma', lang='es', use_gpu=True)

#descarga de paquete de palabras para omitir
stopwords.words('spanish')

#========= MODULOS =================
nlp=spacy.load('es_core_news_lg')

#data = pd.read_json('tweets\juan pari.json', lines=True)
def find_entities(data):
    Entidades={}
    for tweet in data['text']:
        #Text = Text.replace('\n', ' ')
        doc = nlp(tweet)
        for token in doc.ents:
            if(token.label_=="ORG" or token.label_=="PER" or token.label_=="LOC"):
            #print(token.text, token.label_)
                if token.lemma_ in Entidades:
                    Entidades[str(token.lemma_)] += 1
                else:
                    Entidades[token.lemma_] = 1
    return Entidades


