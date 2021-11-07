import spacy
import mysql.connector
from decouple import config

import localtwitter

DATABASE_NAME = "Full_Run_DB_00"
TWEETS_PER_BATCH = 2000

spa_nlp = spacy.load("en_core_web_lg")
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=DATABASE_NAME)
cursor = cnx.cursor()

i = 0
while(True):
	cursor.execute("SELECT * FROM tweet WHERE processed=0 LIMIT {};".format(TWEETS_PER_BATCH))
	for tweet in cursor.fetchall():
		localtwitter.processTweetForNamedEntities(cnx, spa_nlp, tweet)
	i += 1
	print("processed {} tweets".format(i*2000))