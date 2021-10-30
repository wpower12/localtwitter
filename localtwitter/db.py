from datetime import datetime


def createTables(cnx):

	pass


def storeTweet(cnx, tweet):
	insert_user = ("INSERT IGNORE INTO `localized_twitter`.`user` "
		"(`id`,`name`,`screen_name`,`location`,`followers_count`,`created_at`, `statuses_count`) "
		"VALUES "
		"(%(id)s, %(name)s, %(screen_name)s, %(location)s, %(followers_count)s, %(created_at)s, %(statuses_count)s)")

	insert_tweet = ("INSERT IGNORE INTO `localized_twitter`.`tweet` "
		"(`id`,`userid`,`created_at`,`text`) "
		"VALUES (%(id)s, %(userid)s, %(created_at)s, %(text)s)")

	insert_hash = ("INSERT IGNORE INTO `localized_twitter`.`hashtag` "
		"(`text`)"
		"VALUES (%(text)s)")

	insert_tweethash = ("INSERT IGNORE INTO `localized_twitter`.`tweethashtags` "
		"(`tweetid`, `hashtag`)"
		"VALUES (%(tweetid)s, %(hashtag)s)")

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

	if( tweet.entities != None ):
		for hashtag in tweet.entities['hashtags']:
			data_hash = {
				'text' : hashtag['text']
			}
			data_tweethash = {
				'tweetid': tweet.id,
				'hashtag': hashtag['text']
			}

			cursor.execute(insert_hash, data_hash)
			cursor.execute(insert_tweethash, data_tweethash)

	cnx.commit()
	cursor.close()