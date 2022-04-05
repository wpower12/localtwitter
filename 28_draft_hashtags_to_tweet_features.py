import mysql.connector
from decouple import config

from nltk.sentiment.vader import SentimentIntensityAnalyzer

HASHTAG_FN = "data/hashtag_topics.csv"
OUTPUT_FN  = "data/test_tweet_ht_features_w_sent_fips.csv"

# DATABASE_NAME = "Full_Run_DB_00" # Local.
DATABASE_NAME = "Full_Run_01" # For lab machine
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=DATABASE_NAME)


hashtags = [] # Need to maintain the ordering here. 
with open(HASHTAG_FN, 'r') as in_f:
	in_f.readline()
	for line in in_f.readlines():
		hashtag = line.replace("#", "").split(",")[0]
		hashtags.append(hashtag)
num_hashtags = len(hashtags)

GET_TWEETS_KW = """
	SELECT id, created_at, text, countyfips FROM tweet_fti WHERE text LIKE '%{}%';
"""

sid = SentimentIntensityAnalyzer()
curr_ht = 0 # so we can index into each tweets results row
tweet_data = dict()
for ht in hashtags:
	print("processing {}".format(ht))
	cursor = cnx.cursor()
	cursor.execute(GET_TWEETS_KW.format(ht))

	for tweet in cursor:
		tweet_id = tweet[0]
		tweet_dt = tweet[1]
		tweet_text = tweet[2]
		tweet_fips = tweet[3]
		score = sid.polarity_scores(tweet_text)['compound']

		if tweet_id not in tweet_data:
			tweet_data[tweet_id] = {
				'datetime': tweet_dt,
				'score': score,
				'fips': tweet_fips,
				'ht_data': [0 for i in range(num_hashtags)]
			}
		tweet_data[tweet_id]['ht_data'][curr_ht] = 1

	curr_ht += 1 # maintain the index
	print("processed {}, {}/{}".format(ht, curr_ht, num_hashtags))

with open(OUTPUT_FN, 'w') as out_f:
	# Write header row
	#	- Iterate over hashtags and add them to a string
	#   - write it to the file
	header_str = "tweet_id, created_at, sentiment, fips"
	header_str += ", ".join(hashtags)
	out_f.write(header_str+"\n")

	for tweet_id in tweet_data:
		tweet_row = tweet_data[tweet_id]

		tweet_dt   = tweet_row['datetime']
		tweet_sen  = tweet_row['score'] 
		tweet_fips = tweet_row['fips'] 
		tweet_hts = [str(i) for i in tweet_row['ht_data']]

		tweet_str = "{}, {}, {}, {}".format(tweet_id, tweet_dt, tweet_sen, tweet_fips)
		tweet_str += ", ".join(tweet_hts)

		out_f.write(tweet_str+"\n")
