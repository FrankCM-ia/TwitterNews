import re
import spacy

def clean_text(text):
    new_text = spr_emoji(text)
    new_text = new_text.lower() 
    #new_text = NER(new_text)
    new_text = spr_punctuation(new_text)
    new_text = re.sub('http\S+', ' ', new_text)
    new_text = re.sub("\\s+", ' ', new_text)
    #new_text = re.sub("\d+", ' ', new_text)
    return new_text

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

PO = " puto mierda cmtre puta jaja jajaja jajajaja jajajajajajar"


# nlp = spacy.load("es_core_news_sm")
# def NER(text):
#   # encontrar entidades
#   doc = nlp(text)
#   entities = []
#   for ent in doc.ents:
#     entities.append(str(ent))
  
#   # limpiar de signo
#   text = spr_punctuation(text)
  
#   # insertar las ent con subguiones
#   for ent in entities:
#     tmp = ent.replace(' ', '_')
#     text = re.sub(ent,tmp,text)

#   return text



#texto = "Vamos mi Júnior contigo siempre  Feliz cumpleaño en tus 97 años desde Panamá #LALIGAxWIN"
#print(NER(texto))