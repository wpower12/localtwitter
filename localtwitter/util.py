def pprintTweet(tweet):
	print("{}, {}".format(tweet.user.screen_name, tweet.user.name))
	print("\t{}".format(tweet.user.location))

	print("\t{}".format(tweet.id))
	print("\t{}".format(tweet.text))
	print("\t{}".format(tweet.created_at))


def read_csv_to_dict(fn):
	ret = {}
	with open(fn) as f:
		# Read off the first line with col names.
		f.readline()
		for line in f.readlines():
			vals = line.strip().split(",")
			ret[vals[0]] = vals[1]
	return ret

