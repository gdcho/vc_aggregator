import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

twitter_api_key = os.getenv("TWITTER_API_KEY")
twitter_api_secret = os.getenv("TWITTER_API_SECRET")
twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
twitter_access_secret = os.getenv("TWITTER_ACCESS_SECRET")

auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)
api = tweepy.API(auth)

# Fetch tweets
tweets = api.user_timeline(screen_name='username', count=10)  # Replace 'username'
for tweet in tweets:
    print(tweet.text)
