import stanza
from nltk.stem.snowball import SnowballStemmer
#stanza.download('es', package='ancora', processors='tokenize, mwt, pos, lemma', verbose=True)
import spacy
import spacy_spanish_lemmatizer

# Encuentra el lemma de la palabra
stNLP = stanza.Pipeline(processors='tokenize,mwt,pos,lemma', lang='es', use_gpu=True)
def lemmatize(string):
    doc = stNLP(string)
    a = doc.sentences[0].words
    return a[0].lemma

nlp=spacy.load("es_core_news_sm")
# nlp.replace_pipe("lemmatizer", "spanish_lemmatizer")
# def Lemma(word):
#     doc = nlp(word)
#     return doc[0].lemma_

def Tagging(Texto, Tipos):    
  Doc = nlp(Texto)
  Aux = ""
  for Palabra in Doc:
    if(Palabra.pos_ in Tipos):      
      Aux=Aux+str(Palabra)+" "
  return Aux[0:len(Aux)-1]


# Extraer el steming de cada palabra
spanishStemmer=SnowballStemmer("spanish", ignore_stopwords=True)
def stemming(string):
    return spanishStemmer.stem(string)



#text = "#Noticia Nuevo jefe de asesores en el Ministerio de Vivienda es investigado por presunto crimen organizado y lavado de activos https://t.co/RkrwX3Bj9C"
#doc = nlp(text)
#aux = list(doc.ents)
#words = " ".join([str(i) for i in aux])
#words = " ".join([w for w in list(doc.ents)])
#print(words)


