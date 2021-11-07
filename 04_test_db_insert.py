import time
import tweepy
import mysql.connector
from datetime import datetime
from decouple import config

import localtwitter

# Twitter API Connection
auth = tweepy.OAuthHandler(config('T_CONSUME_KEY'), config('T_CONSUME_SECRET'))
auth.set_access_token(config('T_ACCESS_KEY'), config('T_ACCESS_SECRET'))

api = tweepy.API(auth)

# DB Connection
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=config('DB_DATABASE'))


# To, hopefully, avoid RateLimit issues by wrapping the Cursor/Pager.
def limited_cursor(cursor, window_len, num_per_window):
	wait_time = (window_len/(num_per_window+1)) # in seconds
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


def storeTweet(cnx, tweet):
	insert_user = ("INSERT IGNORE INTO `localized_twitter`.`user` "
		"(`id`,`name`,`screen_name`,`location`,`followers_count`,`created_at`, `statuses_count`) "
		"VALUES "
		"(%(id)s, %(name)s, %(screen_name)s, %(location)s, %(followers_count)s, %(created_at)s, %(statuses_count)s)")

	insert_tweet = ("INSERT IGNORE INTO `localized_twitter`.`tweet` "
		"(`id`,`userid`,`created_at`,`text`) "
		"VALUES (%(id)s, %(userid)s, %(created_at)s, %(text)s)")

	data_user = {
		'id': tweet.user.id,
		'name': tweet.user.name,
		'screen_name': tweet.user.screen_name,
		'location': tweet.user.location,
		'followers_count': tweet.user.followers_count,
		'created_at': datetime.strftime(tweet.user.created_at, '%Y-%m-%d %H:%M:%S'),
		'statuses_count': tweet.user.statuses_count
	}
	data_tweet = {
		'id': tweet.id,
		'userid': tweet.user.id,
		'created_at': datetime.strftime(tweet.created_at, '%Y-%m-%d %H:%M:%S'),
		'text': tweet.text
	}

	cursor = cnx.cursor()
	cursor.execute(insert_user,  data_user)
	cursor.execute(insert_tweet, data_tweet)

	cnx.commit()
	cursor.close()


### Where you define the actual search query.
# geocodes lat/longs:
# bucks county 40.333625,-75.120857
# philly       39.959715,-75.165765
# abington     40.138342,-75.126028
res_cur = tweepy.Cursor(api.search_tweets, "",
			geocode="40.138342,-75.126028,10km",
			count=100).pages()   # Note - Use pages() here not items()

count = 0
# The wrapped Cursor handles paging and rates for us.
for tweets in limited_cursor(res_cur, 15*60, 180):
	for tweet in tweets:
		localtwitter.pprintTweet(tweet)
		storeTweet(cnx, tweet)
		count += 1

print(count)