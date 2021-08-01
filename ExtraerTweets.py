import tweepy
import json
import os
from autenticate import get_auth


#Validacion de los Keys
auth = get_auth()
api = tweepy.API(auth, wait_on_rate_limit_notify=True , wait_on_rate_limit=True)


#Encontrar tweets que son tendencia en el momento actual PERU = 23424919 , delimitador de peru 
trends1 = api.trends_place(23424919)
data = trends1[0]

# tomar los trends
trends = data["trends"]

# Poner los trends en una lista
names = list(set([trend["name"] for trend in trends]))

# top 5
#names = names[:10]
print("Total de Temas", len(names))
print(names)

a = input("Escoge un Tema: ")
names = [a]
print(names)

ntweets = int(input("Cuantos tweets deseas? => "))

for key in names:
    # separamos temas por carpetas
    carpeta = 'tweets/' + str(key)
    graficos = 'Graficas/' + str(key)
    if not(os.path.isdir(carpeta)):
        os.mkdir(carpeta)
        os.mkdir(graficos)

    for tweet in tweepy.Cursor(api.search, q = key, tweet_mode = "extended",  lang = 'es' ).items(ntweets):
        text = tweet.full_text
        if tweet.full_text.startswith('RT'):
            rt = tweet.retweeted_status
            text = rt.full_text
            
        name_file = carpeta + '/' + tweet.id_str + ".txt"
        with open(name_file, 'a', encoding="utf-8") as file:
            file.write(text)
        








