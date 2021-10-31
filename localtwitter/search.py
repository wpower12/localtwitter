import tweepy
import time

from .db   import storeTweet
from .util import pprintTweet

from datetime import datetime


def limited_cursor(cursor, window_len, num_per_window):
	wait_time = (window_len/(num_per_window+1)) # in seconds
	first = True
	while True:
		if not first:
			time.sleep(wait_time)
		else:
			first = False
			
		try:
			yield next(cursor)
		except tweepy.TooManyRequests:
			print("rate limited")
			break
		except StopIteration:
			print("stopped?")
			break


def geocodeSearchAndInsert(cnx, twitter_api, geocode, 
	search_term="", 
	report=True, 
	limit=None, 
	window_len=15*60,
	num_per_window=180):

	res_cursor = tweepy.Cursor(twitter_api.search_tweets, 
			search_term,
			geocode=geocode,
			count=100).pages()   # Note - Use pages() here not items()

	# The wrapped Cursor handles paging and rates for us.
	count = 0
	for tweets in limited_cursor(res_cursor, window_len, num_per_window):
		broke = False
		for tweet in tweets:
			storeTweet(cnx, tweet)
			
			if report:
				pprintTweet(tweet)

			count += 1
			if limit != None and count >= limit:
				broke = True
				break

		if broke:
			break

	return count


def allCountySearchAndInsert(cnx, twitter_api,
	report=True, 
	limit=None, 
	window_len=15*60,
	num_per_window=180):
	
	# first get counties from db.
	cur = cnx.cursor()
	res = cur.execute("SELECT fips, geocode")
	# for each one, craft a geocode, and use the method about to 
	# actually query. 

	pass