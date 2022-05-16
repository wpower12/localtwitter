import time

import mysql.connector
from decouple import config

DATABASE_NAME = "Full_Run_DB_00" # Local.
# DATABASE_NAME = "Full_Run_01" # For lab machine
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=DATABASE_NAME)

CREATE_COL = True
COL_NAME = "dupe_ratio_05"
BATCH_SIZE = 100

ADD_COL_SQL = """
	ALTER TABLE `user` 
	ADD COLUMN `{}` DOUBLE NULL DEFAULT NULL;
""".format(COL_NAME)

COUNT_USERS = """
	SELECT COUNT(*) FROM `user` WHERE {} is NULL;
"""

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

if CREATE_COL:
	cur.execute(ADD_COL_SQL)
	cnx.commit()

cur.execute(COUNT_USERS.format(COL_NAME))
total_users = cur.fetchone()[0]

users_processed = 0
while True:
	batch_start = time.perf_counter()
	cur.execute(GET_USERS_SQL)
	users = cur.fetchall()
	users_processed += len(users)
	if len(users) == 0:
		break

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

		# print(UPDATE_USER.format(COL_NAME, val, user_id))
		cur.execute(UPDATE_USER.format(COL_NAME, val, user_id))
	cnx.commit()

	batch_stop = time.perf_counter()
	time_remaining_est_min = (batch_stop-batch_start)*(total_users-users_processed)/60
	print("{}/{} - {:.2f}".format(users_processed, total_users, time_remaining_est_min))

cnx.close()
