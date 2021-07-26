import re
import json
import os
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
import stanza
#stanza.download('es', package='ancora', processors='tokenize, mwt, pos, lemma', verbose=True)

# Cuenta la incidencias de una lista str respecto a otra lista str
def vectorize(tokens,filtrado): #[hola,mano,que,fue,mano] [hola, mano]
    vector=[]
    for i in filtrado: #[hola,mano]
        vector.append(tokens.count(i))
    return vector #[1,2]

# Esta función devuelve una lista de palabras sin que alguna se repita
def unique(sequence): #[hola,mano,que,fue,mano]
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))] # [hola, hmano, que, fue]


# Funcion que limpia las palabras de caracteres especiales
def spr_punctuation(word):
    # special_char no debe tener espacios
    special_char = "|%»“”#,:;.¿?!¡'/@…()-\""
    regex = '[\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'
    special_char = special_char + regex
    delimit = "_"
    new_word = re.sub(regex , "", word)

    for i in delimit:
        new_word = new_word.replace(i, " ")
    return new_word

# Elimina los emojis de una cadena  # emoticons # symbols & pictographs # transport & map symbols # flags (iOS)
def spr_emoji(string):
    emoji_pattern = re.compile("[" u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF" u"\U0001F680-\U0001F6FF"  u"\U0001F1E0-\U0001F1FF" "]+", flags=re.UNICODE)
    res = emoji_pattern.sub(r'', string)
    res = spr_emojis_NC(res)
    return res

# Elimina los emojis No Considerados
def spr_emojis_NC(string):
    # special_emojis no debe tener espacios
    special_emojis = "❤️⚽🤏🤝✅�🥺❌🤩🤔✌🤨🤡☕☔🤗🤣🤮"
    for i in special_emojis:
        string = string.replace(i, "")
    return string

# Contar palabras en cada tweet
def Count_Word(text, words):
    dic = {}
    for word in words:
        if word in text:
            dic[word]= text.count(word)
    return dic 

# Eliminar links de una cadena de string
def spr_link(tokens):
    tokensV2 = []
    for i in range(0, len(tokens)):
        if not ('htt' in tokens[i]):
          tokensV2.append(tokens[i])
    return tokensV2





