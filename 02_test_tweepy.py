import tweepy
from decouple import config

import localtwitter

auth = tweepy.OAuthHandler(config('T_CONSUME_KEY'), config('T_CONSUME_SECRET'))
auth.set_access_token(config('T_ACCESS_KEY'), config('T_ACCESS_SECRET'))

api = tweepy.API(auth)

# geocodes lat/longs:
# bucks county 40.333625,-75.120857
# philly       39.959715,-75.165765
results = api.search_tweets("", geocode="40.333625,-75.120857,5km")

for s in results:
	localtwitter.pprintTweet(s)
	print("")