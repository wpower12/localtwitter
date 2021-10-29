import tweepy

# Based on the Models from the docs, and reading the json. 
def pprintTweet(tweet):
	print("{}, {}".format(tweet.user.screen_name, tweet.user.name))
	print("\t{}".format(tweet.user.location))

	print("\t{}".format(tweet.id))
	print("\t{}".format(tweet.text))
	print("\t{}".format(tweet.created_at))
	# print("\t{}".format(tweet.place))




def limit_handled(cursor, ):

    while True:
        try:
            yield next(cursor)
        except tweepy.RateLimitError:
        	print("rate limited")
        	break