import time
import tweepy
from decouple import config

import localtwitter

auth = tweepy.OAuthHandler(config('T_CONSUME_KEY'), config('T_CONSUME_SECRET'))
auth.set_access_token(config('T_ACCESS_KEY'), config('T_ACCESS_SECRET'))

api = tweepy.API(auth)

def limit_handled(cursor, window_len, num_per_window):
	wait_time = (window_len/(num_per_window+1)) # in what, seconds? ms?
	print(wait_time)
	while True:
		time.sleep(wait_time)
		try:
			yield next(cursor)
		except tweepy.TooManyRequests:
			print("rate limited")
			break
		except StopIteration:
			print("stopped?")
			break

# geocodes lat/longs:
# bucks county 40.333625,-75.120857
# philly       39.959715,-75.165765
res_cur = tweepy.Cursor(api.search_tweets, "",
			geocode="40.333625,-75.120857,5km").pages()

count = 0
for tweets in limit_handled(res_cur, 15*60, 180):
	# print(tweets)
	for tweet in tweets:
		localtwitter.pprintTweet(tweet)
		count += 1

print(count)