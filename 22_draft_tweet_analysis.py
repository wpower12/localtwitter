import mysql.connector
from decouple import config

import localtwitter

DATABASE_NAME = "Full_Run_DB_00"
# DATABASE_NAME = "Full_Run_01" # For lab machine
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=DATABASE_NAME)

TOPIC_KEYWORD_FN = "data/tweet_keywords.csv"
EXPERIMENT_ID_STR = "test_07"

keywords = []
with open(TOPIC_KEYWORD_FN, 'r') as f:
	for line in f.readlines():
		keywords.append(line.split(" ")[0])

localtwitter.createAnalysisTable(cnx, EXPERIMENT_ID_STR, keywords)
localtwitter.analyizeTweetSentiment(cnx, EXPERIMENT_ID_STR, keywords)
