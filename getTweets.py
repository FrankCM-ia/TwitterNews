import tweepy
import json
import ast

#Validacion de los Keys
def get_auth():
    consumer_key = 'yaYuXILlXoN7HxmDtEc1T2nmd'
    consumer_secret = 'Euok5MTRsFsywOZ1Vtql4OX6YndYwPjUH9gAGJWA1iu2rjFCs6'
    access_token = '1331422495396782085-amY4SseueoOVtuDh9IOPJL6dNf7OCh'
    access_token_secret = '8KzZdRfZ1LHyF1jo0kWc9kCNf9OF9WpV9X6Aqr0DPtD7q'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth
    
# Validacion de usuario
auth = get_auth()
api = tweepy.API(auth, wait_on_rate_limit_notify=True , wait_on_rate_limit=True)

def getTrend():
    #Encontrar tweets que son tendencia en el momento actual PERU = 23424919 , delimitador de peru 
    data = api.trends_place(418440)[0]

    #tomar los top trends
    trends = {dic['name']:dic['tweet_volume'] for dic in data['trends']}
    top_trends = sorted(trends)
    print("[✓] Trends successfully extracted.")
    return top_trends

# TEMAS
def get_topics():
    return ['deportes', 'politica peru', 'economia peru', 'ultimas noticias', 'juegos', 'vacunacion peru', 'noticias cusco', 'tecnologia', 'serie', 'pelicula']

# top_trends += temas

# Obtener tweets 
def get_tweets_tweepy(trend, items=500):

    # Parametros de Cursor: -filter:retweets , result_type = "popular"
    with open("tweets/" + trend + '.json', 'a', encoding='utf-8') as file:
        for tweet in tweepy.Cursor(api.search, q = trend + '-filter:retweets filter:media', tweet_mode = "extended", lang = 'es', result_type = "mixed").items(items):
            dic = {}
            dic["id"] = tweet.id_str
            text = tweet.full_text
            if tweet.full_text.startswith('RT'):
                try:
                    rt = tweet.retweeted_status
                    text = rt.full_text
                except:
                    pass
            dic["text"] = text
            dic["screen_name"] = tweet.user.screen_name
            dic["name"] = tweet.user.name 
            dic["user_followers"] = tweet.user.followers_count
            dic["retweet_count"] = tweet.retweet_count
            dic["favorite_count"] = tweet.favorite_count
            dic["date"] = str(tweet.created_at)
            dic["language"] = tweet.lang
            entities = ast.literal_eval(json.dumps(tweet.entities))
            try:
                dic["img"] = entities['media'][0]['media_url']
            except:
                dic["img"] = ''
            json.dump(dic, file)
            file.write('\n')
    print('[✓] ' + str(items) + ' tweets received about '+ trend)

#get_tweets_tweepy("spiderman")