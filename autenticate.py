import tweepy

def get_auth():
    consumer_key = 'yaYuXILlXoN7HxmDtEc1T2nmd'
    consumer_secret = 'Euok5MTRsFsywOZ1Vtql4OX6YndYwPjUH9gAGJWA1iu2rjFCs6'
    access_token = '1331422495396782085-amY4SseueoOVtuDh9IOPJL6dNf7OCh'
    access_token_secret = '8KzZdRfZ1LHyF1jo0kWc9kCNf9OF9WpV9X6Aqr0DPtD7q'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

