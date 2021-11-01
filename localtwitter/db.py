from datetime import datetime

from .sql import CREATE_TABLES, CREATE_FKS
from .sql import INSERT_USER, INSERT_TWEET, INSERT_COUNTY
from .sql import INSERT_HASH, INSERT_URL, INSERT_TWEETHASH, INSERT_TWEETURL
	
		
def createSchema(cnx, db_name):
	cur = cnx.cursor()

	cur.execute("CREATE DATABASE {};".format(db_name))
	cnx.database = db_name
	print("created db {}".format(db_name))

	for table, create_sql in CREATE_TABLES:
		print(table)
		cur.execute(create_sql)
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
		'countyfips': fips
	}

	data_tweet = {
		'id': tweet.id,
		'userid': tweet.user.id,
		'created_at': datetime.strftime(tweet.created_at, '%Y-%m-%d %H:%M:%S'),
		'text': tweet.text
	}

	cursor = cnx.cursor()
	cursor.execute(INSERT_USER,  data_user)
	cursor.execute(INSERT_TWEET, data_tweet)

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

	cnx.commit()
	cursor.close()