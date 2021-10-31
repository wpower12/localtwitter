from datetime import datetime

TABLES = [
	["user", 
	"""
		CREATE TABLE `user` (
		  `id` bigint NOT NULL,
		  `name` varchar(45) NOT NULL,
		  `screen_name` varchar(45) NOT NULL,
		  `location` varchar(45) NOT NULL,
		  `followers_count` varchar(45) NOT NULL,
		  `created_at` datetime NOT NULL,
		  `statuses_count` int NOT NULL,
		  `countyfips` varchar(5) NOT NULL
		  PRIMARY KEY (`id`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
	"""],
	["tweet", 
	"""
		CREATE TABLE `tweet` (
		  `id` bigint NOT NULL,
		  `userid` bigint NOT NULL,
		  `created_at` datetime NOT NULL,
		  `text` varchar(140) NOT NULL,
		  PRIMARY KEY (`id`),
		  KEY `user` (`userid`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
	"""],
	["hashtag", 
	"""
		CREATE TABLE `hashtag` (
		  `text` varchar(45) NOT NULL,
		  PRIMARY KEY (`text`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

	"""],
	["tweethashtag", 
	"""
		CREATE TABLE `tweethashtags` (
		  `tweetid` bigint NOT NULL,
		  `hashtag` varchar(45) NOT NULL,
		  PRIMARY KEY (`tweetid`),
		  UNIQUE KEY `TH_UNIQUE` (`hashtag`,`tweetid`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
	"""],
	["county",
	"""
		CREATE TABLE `county` (
		  `fips` varchar(5) NOT NULL,
		  `countyname` varchar(55) DEFAULT NULL,
		  `lat` decimal(10,8) DEFAULT NULL,
		  `long` decimal(11,8) DEFAULT NULL,
		  `geocode` varchar(30) DEFAULT NULL,
		  `statename` varchar(45) DEFAULT NULL,
		  `state` varchar(2) DEFAULT NULL,
		  PRIMARY KEY (`fips`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
	"""]]

CREATE_FKS = [
	["user",
	 ["""
		ALTER TABLE `user` 
		ADD CONSTRAINT `fk_couny`
		  FOREIGN KEY (`countyfips`)
		  REFERENCES `county` (`fips`)
		  ON DELETE NO ACTION
		  ON UPDATE NO ACTION;
		"""]],
	["tweet", 
	 ["""
		ALTER TABLE `tweet` 
		ADD CONSTRAINT `user_fk`
		  FOREIGN KEY (`userid`)
		  REFERENCES `user` (`id`)
		  ON DELETE NO ACTION
		  ON UPDATE NO ACTION;
		"""]],
	["tweethashtag", 
	 ["""
		ALTER TABLE `tweethashtags`
		ADD CONSTRAINT `fk_hashtext` 
		  FOREIGN KEY (`hashtag`) 
		  REFERENCES `hashtag` (`text`)
		  ON DELETE NO ACTION
		  ON UPDATE NO ACTION;
	  """,
	  """
		ALTER TABLE `tweethashtags`
		ADD CONSTRAINT `fk_tweetid`
		  FOREIGN KEY (`tweetid`) 
		  REFERENCES `tweet` (`id`)
		  ON DELETE NO ACTION
		  ON UPDATE NO ACTION;
	  """]]]
		
		
def createSchema(cnx, db_name):
	cur = cnx.cursor()

	cur.execute("CREATE DATABASE {};".format(db_name))
	cnx.database = db_name
	print("created db {}".format(db_name))

	for table, create_sql in TABLES:
		cur.execute(create_sql)
		print("created table {}".format(table))

	for table, fks in CREATE_FKS:
		for fk_sql in fks:
			cur.execute(fk_sql)
		print("created fk's for {}".format(table))

	cnx.commit()
	cursor.close()


def populateCountyTable(cnx, county_df):
	insert_county = (
		"INSERT IGNORE INTO `county`"
		"(`fips`, `countyname`, `lat`, `long`, `geocode`, `statename`, `state`) "
		"VALUES "
		"(%(fips)s, %(countyname)s, %(lat)s, %(long)s, %(geocode)s, %(statename)s, %(state)s)")

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
		cur.execute(insert_county, county_data)

	cnx.commit()
	cur.close()

"""
Inserts (or ignores duplicates) of the User, the Tweet, and its Hashtags.
"""
def storeTweet(cnx, tweet, fips):
	insert_user = ("INSERT IGNORE INTO `user` "
		"(`id`,`name`,`screen_name`,`location`,`followers_count`,`created_at`, `statuses_count`, `countyfips`) "
		"VALUES "
		"(%(id)s, %(name)s, %(screen_name)s, %(location)s, %(followers_count)s, %(created_at)s, %(statuses_count)s, %(countyfips)s)")

	insert_tweet = ("INSERT IGNORE INTO `tweet` "
		"(`id`,`userid`,`created_at`,`text`) "
		"VALUES (%(id)s, %(userid)s, %(created_at)s, %(text)s)")

	insert_hash = ("INSERT IGNORE INTO `hashtag` "
		"(`text`)"
		"VALUES (%(text)s)")

	insert_tweethash = ("INSERT IGNORE INTO `tweethashtags` "
		"(`tweetid`, `hashtag`)"
		"VALUES (%(tweetid)s, %(hashtag)s)")

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