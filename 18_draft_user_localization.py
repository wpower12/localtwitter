import mysql.connector
from decouple import config

USERS_PER_BATCH = 2000

DATABASE_NAME = "Full_Run_01" # For lab machine
# DATABASE_NAME = "Full_Run_DB_00" # Local machine.

cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=DATABASE_NAME)

NON_LOCALED_USERS = """
	SELECT user.id FROM user
	WHERE mode_tweet_fips_00 IS NULL 
	LIMIT {};"""

MODE_TWEET_FIPS = """
	SELECT tweet.countyfips, COUNT(*)
	FROM user
	LEFT JOIN tweet ON tweet.userid=user.id
	WHERE user.id={}
	GROUP BY tweet.countyfips
	ORDER BY COUNT(*) DESC 
	LIMIT 1;"""

UPDATE_USER_TWEET_FIPS = """
	UPDATE user SET `mode_tweet_fips_00`='{}'  
	WHERE `id`={};"""

running = True
i = 1
while running:
	cur = cnx.cursor()
	cur.execute(NON_LOCALED_USERS.format(USERS_PER_BATCH))
	users = cur.fetchall()

	if len(users) == 0:
		running = False
		break

	for user_row in users:
		user_id = user_row[0]
		# print(MODE_TWEET_FIPS.format(user_id))
		cur.execute(MODE_TWEET_FIPS.format(user_id))
		fips_mode = cur.fetchall()[0][0]

		if fips_mode != None:
			cur.execute(UPDATE_USER_TWEET_FIPS.format(fips_mode, user_id))
		else:
			cur.execute(UPDATE_USER_TWEET_FIPS.format("NONE", user_id))
	cnx.commit()
	print("Updated {}".format(i*USERS_PER_BATCH))
	i += 1
