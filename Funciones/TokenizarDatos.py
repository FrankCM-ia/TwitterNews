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

# Extraer el steming de cada palabra
spanishStemmer=SnowballStemmer("spanish", ignore_stopwords=True)
def stemming(string):
    return spanishStemmer.stem(string)
