# =========================================== LIMPIEZA DE DATOS ======================================================
import re
import spacy
#import spacy_spanish_lemmatizer
import os
import wikipedia as wiki
import random
import operator
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
  new_text = without_accents(new_text) 
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
      Aux = Aux + str(Palabra) + ""
  return Aux[0:len(Aux)-1]


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

def get_glossaries():
    glossaries = {}
    with os.scandir('glossaries') as gloss_scanIte:
        for txt in gloss_scanIte:
            tmp = open(txt, 'r').readlines()
            lines = [ without_accents(word.rsplit('\n')[0]) for word in tmp]
            name = txt.path.split('\\')[-1].split('.')[0]
            glossaries[name] = lines
    return glossaries

def eval_top_words(text, set_words):
    text_clean = clean_text(text)
    tokens = text_clean.split()
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
  
def tag_news(text):
    glossaries = get_glossaries()
    point = 0
    tag = 'otros'
    for key in glossaries:
      if key != 'zbad':
        c = eval_top_words(text, glossaries[key])
        if c > point:
          point = c
          tag = key
      else:
        c = eval_top_words(text, glossaries[key])
        point = point - c
    if point <= 0: tag = 'otros'
    return tag + ' ' + str(point)

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

def find_top_group(data):
    data_top_by_favorite = data.sort_values('favorite_count', ascending=False)
    top_tweets_by_favorite = { k:2 for k in data_top_by_favorite['id'].head(10)}

    data_top_by_user_followers = data.sort_values('user_followers', ascending=False)
    top_tweets_by_user_followers = { k:3 for k in data_top_by_user_followers['id'].head(10)} 

    data_top_by_retweet_count = data.sort_values('retweet_count', ascending=False)
    top_tweets_by_retweet_count = { k:1 for k in data_top_by_retweet_count['id'].head(10)}

    data_score = data.copy()
    data_score['score'] = data_score['user_followers'] * data_score['retweet_count'] * data_score['favorite_count']
    top_tweets_by_score = { k:4 for k in data_score['id'].head(10)}

    ids = set(top_tweets_by_favorite.keys()) | set(top_tweets_by_user_followers.keys()) | set(top_tweets_by_retweet_count.keys()) | set(top_tweets_by_score.keys())
    headlines = {}
    for id in ids:
        fa = get_value(top_tweets_by_favorite, id)
        uf = get_value(top_tweets_by_user_followers, id)
        rc = get_value(top_tweets_by_retweet_count, id)
        sc = get_value(top_tweets_by_score, id)
        headlines[id] = fa + uf + rc + sc
    top_headlines = sorted(headlines.items(), key = operator.itemgetter(1), reverse=True)[:10]
    top_headlines_dic = { i[0]:i[1]  for i in top_headlines}

    data_headlines =  data[data.id.isin(list(top_headlines_dic.keys()))]
    data_headlines['score'] = [ top_headlines_dic[id] for id in data_headlines['id']]
    top_data_headlines = data_headlines.sort_values('score', ascending=False)
    return top_data_headlines

# Noticia
def create_new(row_data_news):
    new = {}
    new['id'] = row_data_news['id']
    new['title'] = row_data_news['text']
    new['date'] = str(row_data_news['date'])
    new['screen_name'] = row_data_news['screen_name']
    new['name'] = row_data_news['name']
    new['img'] = row_data_news['img']
    new['url'] = row_data_news['url']
    new['category'] = row_data_news['tag']
    new['score one'] = row_data_news['sum_p']
    new['score two'] = row_data_news['user_followers']
    return new
#text = "#Noticia Nuevo jefe de asesores en el Ministerio de Vivienda es investigado por presunto crimen organizado y lavado de activos https://t.co/RkrwX3Bj9C"
#doc = nlp(text)
#aux = list(doc.ents)
#words = " ".join([str(i) for i in aux])
#words = " ".join([w for w in list(doc.ents)])
#print(words)


# # Definir stopwords
# stop_word_es = get_stop_words('spanish')
# def find_top_words(data):
#     # contabilizar frecuencias mediante CV
#     cv = CountVectorizer(stop_words= stop_word_es)
#     cv_matrix = cv.fit_transform(data['text'])
#     count_words = np.sum(cv_matrix.toarray(), axis=0)
#     words_cv =  {key:count_words[cv.vocabulary_[key]] for key in cv.vocabulary_}
#     top_words_cv = sorted(words_cv.items(), key=operator.itemgetter(1), reverse=True)

#     # contabilizar frecuencia mediante IDF
#     tfidf = TfidfTransformer()
#     tfidf_matrix = tfidf.fit_transform(cv_matrix)
#     words_idf =  dict(zip(cv.get_feature_names(), tfidf.idf_))
#     top_words_idf =  sorted(words_idf.items(), key=operator.itemgetter(1), reverse=True)
#     return top_words_cv, top_words_idf