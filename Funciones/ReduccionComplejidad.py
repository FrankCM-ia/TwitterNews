import stanza
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

#stanza.download('es', package='ancora', processors='tokenize, mwt, pos, lemma', verbose=True)

# Encuentra el lemma de la palabra
stNLP = stanza.Pipeline(processors='tokenize,mwt,pos,lemma', lang='es', use_gpu=True)
def lemmatize(string):
    doc = stNLP(string)
    a = doc.sentences[0].words
    return a[0].lemma

spanishStemmer=SnowballStemmer("spanish", ignore_stopwords=True)
def stemming(string):
    return spanishStemmer.stem(string)

# Encuentra el lemmas a un listado de palabras
def lemmatize_Tokens(tokens):
    for i in range(0,len(tokens)):
        tokens[i] = lemmatize(tokens[i])
    return tokens

# Elimina palabras irrelevantes de una lista de palabras
def spr_StopWords(tokens):
    stop_words = stopwords.words('spanish')
    special_stopwords = ['rt']
    stop_words = stop_words + special_stopwords
    tokensV2 = []
    for i in range(0, len(tokens)) : 
        if not (tokens[i] in stop_words):
            tokensV2.append(tokens[i])
    tokensV2 = spr_OneLetter(tokensV2)
    return tokensV2

#Elimina tokens q solo es una letra
def spr_OneLetter(tokens):
    tokensV2 = []
    for i in range(0, len(tokens)):
        if (len(tokens[i])!=1):
          tokensV2.append(tokens[i])
    return tokensV2
