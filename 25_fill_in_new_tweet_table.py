import mysql.connector
from decouple import config

# DATABASE_NAME = "Full_Run_DB_00" # Local.
DATABASE_NAME = "Full_Run_01" # For lab machine
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=DATABASE_NAME)

BATCH_SIZE = 500

SQL_GET_TWEETS = """
	SELECT `id`, `userid`, `created_at`, `text`, `countyfips` FROM tweet
	WHERE tweet.copied IS NULL
	LIMIT {};"""

# Note - The parameter here must be filled with a comma seperated list
# of the rows to be inserted, each in its own parens.
SQL_INSERT_TFTI = """
	INSERT INTO `tweet_fti`
	(`id`,
	`userid`,
	`created_at`,
	`text`,
	`countyfips`,
	`sentiment_flag`) 
	VALUES
	{};
"""

# Note - The parameter here is a comma seperated list/string of the
# ids for all the 'copied' tweets. 
SQL_UPDATE_FLAGS = """
	UPDATE tweet
	SET tweet.copied = 1
	WHERE tweet.id IN ({});
"""

i = 0
running = True
while(running):

	cursor = cnx.cursor()
	cursor.execute(SQL_GET_TWEETS.format(BATCH_SIZE))
	tweet_batch = cursor.fetchall()

	if(len(tweet_batch) == 0):
		running = False
		break

	# These will turn into the strings that we pass to the INSERT and UPDATE queries.
	tweet_id_str = ""
	insert_str   = "" 

	for tweet in tweet_batch:
		tweet_id = tweet[0]
		user_id  = tweet[1]
		created  = tweet[2]
		text     = tweet[3]
		fips     = tweet[4]

		tweet_id_str += "{}, ".format(tweet_id)
		insert_str   += "({}, {}, {}, {}, {}), ".format(tweet_id,
			user_id,
			created,
			text,
			fips)

	tweet_id_str = tweet_id_str[:-2]
	insert_str = insert_str[:-2] 

	cursor.execute(SQL_INSERT_TFTI.format(insert_str))
	cursor.execute(SQL_UPDATE_FLAGS.format(tweet_id_str))

	cnx.commit()

	i += 1
	print("copied {}".format(i*BATCH_SIZE))