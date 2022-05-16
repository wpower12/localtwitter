import mysql.connector
from decouple import config

DATABASE_NAME = "Full_Run_DB_00" # Local.
# DATABASE_NAME = "Full_Run_01" # For lab machine
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=DATABASE_NAME)

COL_NAME = "dupe_ratio_02"
BATCH_SIZE = 1000

ADD_COL_SQL = """
	ALTER TABLE `user` 
	ADD COLUMN `{}` DOUBLE NULL DEFAULT NULL;
""".format(COL_NAME)

GET_USERS_SQL = """
	SELECT id FROM `user` WHERE {} is NULL LIMIT {};
""".format(COL_NAME, BATCH_SIZE)

COUNT_USER_TWEETS = """
	SELECT COUNT(*) 
	FROM tweet
	WHERE userid={};
"""

GET_USER_TWEETS = """
	SELECT text, COUNT(*) 
	FROM tweet
	WHERE userid={}
	GROUP BY text
	HAVING COUNT(*) > 1;
"""

UPDATE_USER = """
	UPDATE `user` SET `{}`={}
	WHERE `id`={};
"""

# Create the column for the result ratio.
cur = cnx.cursor()
cur.execute(ADD_COL_SQL)
cnx.commit()
cur.close()

i = 0
while True:
	cur = cnx.cursor()
	cur.execute(GET_USERS_SQL)
	users = cur.fetchall()

	for user in users:
		user_id = user[0]
		cur.execute(COUNT_USER_TWEETS.format(user_id))
		count = cur.fetchone()[0]

		cur.execute(GET_USER_TWEETS.format(user_id))
		total = 0
		for dupe_tweet in cur.fetchall():
			total += dupe_tweet[1]

		val = 0.0
		if count > 0:
			val = float(total)/float(count)

		print(UPDATE_USER.format(COL_NAME, val, user_id))
		break
		# cur.execute(UPDATE_USER.format(COL_NAME, val, user_id))
	cnx.commit()

	i += 1
	print("{}".format(i*BATCH_SIZE))

# For each user
	# Get count of number of tweets
	# Get count of duplicate tweets
		# So sum all the group-bys that have a count larger than 2.
	# Save out ratio