import mysql.connector
from decouple import config

DATABASE_NAME = "Full_Run_DB_00" # Local.
# DATABASE_NAME = "Full_Run_01" # For lab machine
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=DATABASE_NAME)

OUTPUT_FN = "data/tweets_by_threshold.txt"
COL_NAME = "dupe_ratio_02"

COUNT_THRESH_SQL = """
	SELECT COUNT(*) FROM tweet
	LEFT JOIN user ON user.id=tweet.userid
	WHERE user.{} <= {};
"""
THRESHOLDS = [i*0.05 for i in range(0, 20+1)]

with open(OUTPUT_FN, 'w') as f:
	f.write("threshold, tweet_count\n")
	cur = cnx.cursor()
	for t in THRESHOLDS:
		cur.execute(COUNT_THRESH_SQL.format(COL_NAME, t))
		v = cur.fetchone()[0]
		f.write("{}, {}\n".format(t, v))
