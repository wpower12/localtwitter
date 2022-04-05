import mysql.connector
from decouple import config

OUTPUT_FN = "data/test_user_kw_features.csv"
USER_BATCH_SIZE = 500
KEYWORDS = ["test", "trump", "biden", "ukraine"]

DATABASE_NAME = "Full_Run_DB_00" # Local.
# DATABASE_NAME = "Full_Run_01" # For lab machine
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=DATABASE_NAME)


# Find batch of users who haven't been processed.
# "SELECT" the user_id and FIPS location

# FIND_USERS = """
# 	SELECT id, mode_tweet_fips_00 FROM user
# 	WHERE keywords_processed=0;
# """
FIND_USERS = """
	SELECT user.id, user.countyfips FROM user 
	WHERE user.keywords_processed=0 
	LIMIT {};
""".format(USER_BATCH_SIZE)


# for a user_id and keyword pair, find all the tweets by that
# user that contain that keyword, or "LIKE" that keyword
# "SELECT" the tweet sentiment.
# Params = {userid, keyword}

# TWEETS_BY_USERKW = """
# 	SELECT text FROM tweet_fti
# 	WHERE userid={} AND text LIKE '%{}%';
# """
TWEETS_BY_USERKW = """
	SELECT text FROM tweet
	WHERE userid={} AND text LIKE '%{}%';
"""

UPDATE_USERFLAG = """
	UPDATE user
	SET keywords_processed=1
	WHERE id={}; 
"""


def getSentiment(tweet_text):
	# TODO - Make this do VADER stuff. 
	return 1	


user_data = []
while(True):
	with open(OUTPUT_FN, 'a') as out_f:
		cursor = cnx.cursor()
		cursor.execute(FIND_USERS)
		users = cursor.fetchall()

		if(len(users)==0):
			break

		for user in users:
			user_id   = user[0]
			user_fips = user[1]
			user_row = [user_id, user_fips]

			for kw in KEYWORDS:
				cursor.execute(TWEETS_BY_USERKW.format(user_id, kw))
				tweets = cursor.fetchall()

				if(len(tweets) == 0):
					user_row.append(0)
					continue

				num_tweets = len(tweets)
				sent_sum = 0
				for tweet in tweets:
					sent_sum += getSentiment(tweet[0])
				user_row.append(sent_sum/num_tweets)

			user_str = [str(s) for s in user_row]
			user_str = ", ".join(user_str)+"\n"
			out_f.write(user_str)

			user_data.append(user_row)
			cursor.execute(UPDATE_USERFLAG.format(user_id))
			cnx.commit()
