

def pprintTweet(tweet):
	print("{}, {}".format(tweet.user.screen_name, tweet.user.name))
	print("\t{}".format(tweet.user.location))

	print("\t{}".format(tweet.id))
	print("\t{}".format(tweet.text))
	print("\t{}".format(tweet.created_at))
