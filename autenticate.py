import tweepy

def get_auth():
    consumer_key = 'YmMGLkHaHt9qTH68Qlk0ZgYVF'
    consumer_secret = 'PootVOH2wDziq5I9qhk34iHYux8KwymUalSXdMYCCyTl8X39n1'
    access_token = '1404983823142637568-Bx7w4WrZpOJ8Hude68DmozTUeD6vYo'
    access_token_secret = 'TbsXhrCZkHThRBIzkSS3ULiVbYrYDDIY4s0Elv8N93W90'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

