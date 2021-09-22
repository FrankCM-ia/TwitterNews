# =========================================== LIMPIEZA DE DATOS ======================================================
import re
import os
import wikipedia as wiki
import random
wiki.set_lang('es')

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
    special_emojis = "❤️⚽🤏🤝✅�🥺❌🤩🤔✌🤨🤡☕☔🤗🤣🤮🥳🥈⏰🆚🤬✍⏭⚪"
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
  #new_text = without_accents(new_text) 
  new_text = clean_url(new_text)
  new_text = spr_emoji(new_text)
  new_text = spr_punctuation(new_text)
  new_text = re.sub("\\s+", ' ', new_text) # del espacios en
  new_text = re.sub("\d+", ' ', new_text) 
  return new_text

def clean_text_for_enti(text): 
  new_text = clean_url(text)
  new_text = spr_emoji(new_text)
  new_text = spr_punctuation(new_text)
  new_text = re.sub("\\s+", ' ', new_text) # del espacios en
  new_text = re.sub("\d+", ' ', new_text) 
  return new_text

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

# Extraer el steming de cada palabra
spanishStemmer=SnowballStemmer("spanish", ignore_stopwords=True)
def stemming(string):
  return spanishStemmer.stem(string)

def find_mean(word):
  try:
    mean = wiki.summary(word, sentences = 1)
  except wiki.DisambiguationError as e:
    try:
      word = random.choice(e.options)
      mean = wiki.summary(word, sentences = 1)
    except:
      mean = ""
  except wiki.PageError:
    mean = ""
  return mean

def get_value(dict, key):
  try:
    return dict[key]
  except:
    return 0

def eval_top_words(text, set_words):
  text_clean = clean_text(text)
  tokens = [ lemmatize(token) for token in text_clean.split()]
  c = 0
  for token in tokens:
    if token in set_words:
      c += 1
  return c

#cargar glosarios
def get_glossaries():
    glossaries = {}
    with os.scandir('glossaries') as gloss_scanIte:
        for txt in gloss_scanIte:
            tmp = open(txt, 'r').readlines()
            lines = [ without_accents(word.rsplit('\n')[0]) for word in tmp]
            name = txt.path.split('\\')[-1].split('.')[0]
            glossaries[name] = lines
    return glossaries

def get_url(text):
    links = []
    tokens = text.split()
    for token in tokens:
        if token.startswith('http'):
            links.append(token)
    if len(links) == 0:
        return ""
    else:
        return links
