import tweepy


# Pretty Print a Tweet
def pprintTweet(tweet):
	print("{}, {}".format(tweet.user.screen_name, tweet.user.name))
	print("\t{}".format(tweet.user.location))

	print("\t{}".format(tweet.id))
	print("\t{}".format(tweet.text))
	print("\t{}".format(tweet.created_at))


# Rate-Limited Cursor.
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