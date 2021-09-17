# =========================================== LIMPIEZA DE DATOS ======================================================
import re
import spacy
import spacy_spanish_lemmatizer

# Funcion que limpia las palabras de caracteres especiales
def spr_punctuation(word):
    # special_char no debe tener espacios 
    special_char = '\\|\\%\\»\\“\\”\\#\\,\\:\\;\\.\\¿\\?\\!\\¡\\/\\@\\…\\(\\)\\>\\<\\▶\\➡\\€\\►'
    regex = '[\\!\\"\\_\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\' + special_char +'\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\¡\\^\\`\\{\\|\\}\\~]'
    new_word = re.sub(regex , " ", word)
    return new_word

# Elimina los emojis de una cadena  # emoticons # symbols & pictographs # transport & map symbols # flags (iOS)
def spr_emoji(string):
    emoji_pattern = re.compile("[" u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF" u"\U0001F680-\U0001F6FF"  u"\U0001F1E0-\U0001F1FF" u"\u200d♂…" "]+", flags=re.UNICODE)
    res = emoji_pattern.sub(r'', string)
    res = spr_emojis_NC(res)
    return res

# Elimina los emojis No Considerados
def spr_emojis_NC(string):
    # special_emojis no debe tener espacios
    special_emojis = "❤️⚽🤏🤝✅�🥺❌🤩🤔✌🤨🤡☕☔🤗🤣🤮🥳🥈⏰🆚🤬✍⏭"
    for i in special_emojis:
        string = string.replace(i, "")
    return string

def clean_url(text):
  aux = text.split()
  new = []
  for i in aux:
    if not (i.startswith('http') or i.startswith('hah')):
      new.append(i)
  return ' '.join(new)

s = 'áéí el niño está en el avión'
a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN'
trans = str.maketrans(a,b)
def without_accents(text):
    return text.translate(trans)

def clean_text(text):
  new_text = text.lower()
  new_text = without_accents(new_text)
  new_text = clean_url(new_text)
  new_text = spr_emoji(new_text)
  new_text = spr_punctuation(new_text)
  new_text = re.sub("\\s+", ' ', new_text) # del espacios en
  new_text = re.sub("\d+", ' ', new_text) 
  return new_text

# =========================================== TAG and NERD ======================================================


nlp = spacy.load("es_core_news_sm")
def NER(text):
  # encontrar entidades
  doc = nlp(text)
  entities = []
  for ent in doc.ents:
    entities.append(str(ent))
  
  # limpiar de signo
  text = spr_punctuation(text)
  
  # insertar las ent con subguiones
  for ent in entities:
    tmp = ent.replace(' ', '_')
    text = re.sub(ent,tmp,text)

  return text



#texto = "Vamos mi Júnior contigo siempre  Feliz cumpleaño en tus 97 años desde Panamá #LALIGAxWIN"
#print(NER(texto))

#=========================================== TOKENIZACION DE DATOS ====================================================
import stanza
from nltk.stem.snowball import SnowballStemmer
#stanza.download('es', package='ancora', processors='tokenize, mwt, pos, lemma', verbose=True)


# Encuentra el lemma de la palabra
stNLP = stanza.Pipeline(processors='tokenize,mwt,pos,lemma', lang='es', use_gpu=True)
def lemmatize(string):
    doc = stNLP(string)
    a = doc.sentences[0].words
    return a[0].lemma

#nlp=spacy.load("es_core_news_sm")
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