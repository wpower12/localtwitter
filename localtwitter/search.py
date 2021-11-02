import tweepy
import time

from .db   import storeTweet
from .util import pprintTweet

from datetime import datetime


def limited_cursor(cursor, window_len, num_per_window):
	wait_time = (window_len/(num_per_window+2)) # in seconds
	while True:
		time.sleep(wait_time)
		try:
			yield next(cursor)
		except StopIteration:
			# print("stopped.")
			break


def geocodeSearchAndInsert(cnx, twitter_api, geocode,
	fips="", 
	search_term="", 
	since_id=None,
	report=False, 
	limit=None, 
	window_len=15*60,
	num_per_window=180):

	res_cursor = tweepy.Cursor(twitter_api.search_tweets, 
			search_term,
			geocode=geocode,
			since_id=since_id,
			count=100).pages()   # Note - Use pages() here not items()

	# The wrapped Cursor handles paging and rates for us.
	count = 0
	for tweets in limited_cursor(res_cursor, window_len, num_per_window):
		broke = False
		try:
			for tweet in tweets:
				storeTweet(cnx, tweet, fips)
				
				if report:
					pprintTweet(tweet)

				count += 1
				if limit != None and count >= limit:
					broke = True
					break

		except tweepy.error.TooManyRequests:
			print("rate limited")
			break

		if broke:
			break

	return count


def allCountySearchAndInsert(cnx, twitter_api,
	report=True,
	distance="5km", 
	limit=None):
	
	# first get counties from db.
	cur = cnx.cursor()
	cur.execute("SELECT fips, geocode, countyname, state, last_tweet_id FROM county;")
	total_tweets = 0
	for fips, geo, cname, state, last_tweet in cur.fetchall():
		geocode="{},{}".format(geo, distance)
		tweets_found = geocodeSearchAndInsert(cnx, twitter_api, geocode, fips=fips, limit=limit, since_id=last_tweet)
		total_tweets += tweets_found
		if(report):
			print("processed {:>15s}, {} - {:6} tweets {:10} total".format(cname, state, tweets_found, total_tweets))

