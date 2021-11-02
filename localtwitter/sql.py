'''
DB Creation SQL. 
'''
CREATE_TABLES = [
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
		  `countyfips` varchar(5) NOT NULL,
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
  		  `last_tweet_id` bigint DEFAULT NULL,
		  PRIMARY KEY (`fips`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
	"""],
	["url",
	"""
		CREATE TABLE `url` (
		  `id` int NOT NULL AUTO_INCREMENT,
		  `urlhash` char(32) NOT NULL,
		  `url` varchar(256) DEFAULT NULL,
		  PRIMARY KEY (`id`),
		  UNIQUE KEY `urlhash_UNIQUE` (`urlhash`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
	"""],
	["tweeturl",
	"""
		CREATE TABLE `tweeturls` (
		  `tweetid` bigint NOT NULL,
		  `urlhash` char(32) NOT NULL,
		  PRIMARY KEY (`tweetid`),
		  KEY `fk_url_idx` (`urlhash`)
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
	  """]],
	["tweeturl", 
	 ["""
		ALTER TABLE `tweeturls`
		ADD CONSTRAINT `fk_tweet` 
		  FOREIGN KEY (`tweetid`) 
		  REFERENCES `tweet` (`id`)
		  ON DELETE NO ACTION
		  ON UPDATE NO ACTION;
	  """,
	  """
		ALTER TABLE `tweeturls`
		ADD CONSTRAINT `fk_url` 
		  FOREIGN KEY (`urlhash`) 
		  REFERENCES `url` (`urlhash`)
		  ON DELETE NO ACTION
		  ON UPDATE NO ACTION;
	  """]]]


'''
Model SQL.
'''
INSERT_COUNTY = (
	"INSERT IGNORE INTO `county`"
	"(`fips`, `countyname`, `lat`, `long`, `geocode`, `statename`, `state`) "
	"VALUES "
	"(%(fips)s, %(countyname)s, %(lat)s, %(long)s, %(geocode)s, %(statename)s, %(state)s)")

INSERT_USER = ("INSERT IGNORE INTO `user` "
	"(`id`,`name`,`screen_name`,`location`,`followers_count`,`created_at`, `statuses_count`, `countyfips`) "
	"VALUES "
	"(%(id)s, %(name)s, %(screen_name)s, %(location)s, %(followers_count)s, %(created_at)s, %(statuses_count)s, %(countyfips)s)")

INSERT_TWEET = ("INSERT IGNORE INTO `tweet` "
	"(`id`,`userid`,`created_at`,`text`) "
	"VALUES (%(id)s, %(userid)s, %(created_at)s, %(text)s)")

INSERT_HASH = ("INSERT IGNORE INTO `hashtag` "
	"(`text`) "
	"VALUES (%(text)s)")

INSERT_TWEETHASH = ("INSERT IGNORE INTO `tweethashtags` "
	"(`tweetid`, `hashtag`) "
	"VALUES (%(tweetid)s, %(hashtag)s)")

INSERT_URL = ("INSERT IGNORE INTO `url` "
	"(`urlhash`, `url`) "
	"VALUES (MD5(%(url_p)s), %(url_p)s)")

INSERT_TWEETURL = ("INSERT IGNORE INTO `tweeturls` "
	"(`tweetid`, `urlhash`)"
	"VALUES (%(tweetid)s, MD5(%(url_p)s))")

UPDATE_COUNTY_LASTTWEET = ("UPDATE `county` "
	"SET `last_tweet_id`=%(last_tweet_id)s "
	"WHERE fips=%(fips)s")