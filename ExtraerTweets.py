import pandas as pd
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
names = names[:3]
#print("Total de Temas", len(names))
print(names)

#a = input("Escoge un Tema: ")
#names = [a]
#print(names)

ntweets = 800 #int(input("Cuantos tweets deseas? => "))

for topic in names:
    # separamos temas por tema
    corpus = 'tweets/' + str(topic)
    graficos = 'Graficas/' + str(topic)

    if not(os.path.isdir(graficos)):
        os.mkdir(graficos)

    dic = {"id":[], "text":[]}
    for tweet in tweepy.Cursor(api.search, q = topic, tweet_mode = "extended",  lang = 'es' ).items(ntweets):
        text = tweet.full_text
        if tweet.full_text.startswith('RT'):
            rt = tweet.retweeted_status
            text = rt.full_text
        
        dic["id"].append(tweet.id_str[14:])
        dic["text"].append(text)
    df = pd.DataFrame(dic["text"], columns=["text"], index=dic["id"])
    df.to_csv(corpus + '.csv', sep=';', encoding='utf-8')
    
        
