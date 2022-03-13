from datetime import datetime

from .sql import CREATE_TABLES, CREATE_FKS
from .sql import INSERT_USER, INSERT_TWEET, INSERT_COUNTY
from .sql import INSERT_HASH, INSERT_URL, INSERT_TWEETHASH, INSERT_TWEETURL
from .sql import INSERT_NAMED_ENTITY, INSERT_TWEET_NE, INSERT_TWEET_MENTION
from .sql import UPDATE_COUNTY_LASTTWEET, IGNORE_COUNTY, RESET_COUNTY_IGNORE
from .sql import SENTIMENT_TABLE_CREATE, SENTIMENT_TABLE_STUB, SENTIMENT_TWEETS
from .sql import SENTIMENT_INSERT, SENTIMENT_SET_FLAG, SENTIMENT_TWEET_COUNT, SENTIMENT_RESET_FLAGS


def createSchema(cnx, db_name, encoding="utf8mb4_0900_ai_ci"):
	cur = cnx.cursor()
	cur.execute("CREATE DATABASE {};".format(db_name))
	cnx.database = db_name
	print("created db {}".format(db_name))

	for table, create_sql in CREATE_TABLES:
		cur.execute(create_sql, {'encoding': encoding})
		print("created table {}".format(table))

	for table, fks in CREATE_FKS:
		for fk_sql in fks:
			cur.execute(fk_sql)
		print("created fk's for {}".format(table))

	cnx.commit()
	cur.close()


def populateCountyTable(cnx, county_df):
	cur = cnx.cursor()
	for county_row in county_df.iterrows():
		county_raw = county_row[1]
		county_data = {
			'fips': county_raw['FIPS'],
			'countyname': county_raw['NAME'],
			'lat': county_raw['lat'],
			'long': county_raw['long'],
			'geocode': "{:.8f},{:.8f}".format(county_raw['lat'], county_raw['long']),
			'statename': county_raw['STATE_NAME'],
			'state': county_raw['STUSAB']
		}
		cur.execute(INSERT_COUNTY, county_data)

	cnx.commit()
	cur.close()


"""
Inserts (or ignores duplicates) of the User, the Tweet, and its Hashtags.
"""
def storeTweet(cnx, tweet, fips):
	data_user = {
		'id': tweet.user.id,
		'name': tweet.user.name,
		'screen_name': tweet.user.screen_name,
		'location': tweet.user.location,
		'followers_count': tweet.user.followers_count,
		'created_at': datetime.strftime(tweet.user.created_at, '%Y-%m-%d %H:%M:%S'),
		'statuses_count': tweet.user.statuses_count,
	}
	
	data_tweet = {
		'id': tweet.id,
		'userid': tweet.user.id,
		'created_at': datetime.strftime(tweet.created_at, '%Y-%m-%d %H:%M:%S'),
		'text': tweet.text,
		'countyfips': fips
	}

	data_lasttweet = {
		'last_tweet_id': tweet.id,
		'fips': fips
	}

	cursor = cnx.cursor()
	cursor.execute(INSERT_USER,  data_user)
	cursor.execute(INSERT_TWEET, data_tweet)
	cursor.execute(UPDATE_COUNTY_LASTTWEET, data_lasttweet)
	cnx.commit()

	if( tweet.entities != None ):
		for hashtag in tweet.entities['hashtags']:
			data_hash = {
				'text' : hashtag['text']
			}
			data_tweethash = {
				'tweetid': tweet.id,
				'hashtag': hashtag['text']
			}
			cursor.execute(INSERT_HASH,      data_hash)
			cursor.execute(INSERT_TWEETHASH, data_tweethash)

		for url in tweet.entities['urls']:
			data_url = {
				'url_p': url['expanded_url']	
			}
			data_tweeturl = {
				'tweetid': tweet.id,
				'url_p': url['expanded_url']
			}
			cursor.execute(INSERT_URL, data_url)
			cursor.execute(INSERT_TWEETURL, data_tweeturl)

		for user_mention in tweet.entities['user_mentions']:
			# Need to insert the mentioned user, lest the FK's in the mention insert error out. 
			data_mentioned_user = {
				'id': user_mention['id'],
				'name': user_mention['name'],
				'screen_name': user_mention['screen_name'],
				'location': "",
				'followers_count': 0,
				'created_at': datetime.strftime(tweet.user.created_at, '%Y-%m-%d %H:%M:%S'), # Just for now. Will make this nullable soon. 
				'statuses_count': 0	
			}
			cursor.execute(INSERT_USER,  data_mentioned_user)

			data_mention = {
				'tweetid': tweet.id,
				'userid': user_mention['id']
			}
			cursor.execute(INSERT_TWEET_MENTION, data_mention)

	cnx.commit()
	cursor.close()


def storeNamedEntity(cnx, tweet_id, named_entity):
	# check if id is there, otherwise make a new one and recover id from cnx 
	ne_string = named_entity.text.replace("'", "")

	cur = cnx.cursor()
	cur.execute("SELECT id, name FROM `namedentity` WHERE name='{}';".format(ne_string))
	nes = cur.fetchall()
	if( len(nes) > 0 ):
		ne_id = nes[0][0]
	else:
		# make a new one
		data_ne = {
			'name': ne_string,
			'type': named_entity.label_
		}
		cur.execute(INSERT_NAMED_ENTITY, data_ne)
		ne_id = cur.lastrowid
		cnx.commit()

	# store the tweet-ne link
	data_tne = {
		'tweetid': tweet_id,
		'nentityid': ne_id,
	}
	cur.execute(INSERT_TWEET_NE, data_tne)

	cnx.commit()
	cur.close()


def setTweetAsProcessed(cnx, tweet_id):
	cur = cnx.cursor()
	cur.execute("UPDATE `tweet` SET processed=1 WHERE id={}".format(tweet_id))


def resetCountyIgnore(cnx):
	cursor = cnx.cursor()
	cursor.execute(RESET_COUNTY_IGNORE)
	# cursor.close()


def ignoreCounty(cnx, fips):
	cursor = cnx.cursor()
	cursor.execute(IGNORE_COUNTY, {'fips': fips})
	
"""
Sentiment Analysis 
"""
def createAnalysisTable(cnx, unq_id, keywords):
	tables = ""
	for keyword in keywords:
		tables += SENTIMENT_TABLE_STUB.format(keyword)
	tables = tables.rstrip()
	FULL_QUERY = SENTIMENT_TABLE_CREATE.format(unq_id, tables)
	cursor = cnx.cursor()
	cursor.execute(FULL_QUERY)


def getTweetCount(cnx):
	cursor = cnx.cursor()
	cursor.execute(SENTIMENT_TWEET_COUNT)
	return cursor.fetchone()[0]


def getSentimentTweetBatch(cnx, batch_size):
	cursor = cnx.cursor()
	cursor.execute(SENTIMENT_TWEETS.format(batch_size))
	return cursor.fetchall()


def insertTweetSentiment(cnx, unq_id, tweet_id, keywords, sent_value):	
	keyword_str = ""
	value_str = ""
	for kw in keywords:
		keyword_str += "{}, ".format(kw)
		value_str += "{}, ".format(sent_value)
	keyword_str = keyword_str[:-2]
	value_str = value_str[:-2]

	# parameters = (sentiment_unqid, keyword_list, tweetid, keyword_values)
	cursor = cnx.cursor()
	cursor.execute(SENTIMENT_INSERT.format(
		unq_id,
		keyword_str,
		tweet_id,
		value_str))
	cnx.commit()


def setSentimentFlag(cnx, tweet_id):
	cursor = cnx.cursor()
	cursor.execute(SENTIMENT_SET_FLAG.format(tweet_id))
	cnx.commit()


def resetSentimentFlags(cnx):
	cursor = cnx.cursor()
	cursor.execute(resetSentimentFlags)
	cnx.commit()
