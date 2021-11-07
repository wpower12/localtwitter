import spacy
import mysql.connector
from decouple import config

import localtwitter

cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=config('DB_DATABASE'))

GET_TWEETS = "SELECT * FROM tweet WHERE processed=0 LIMIT 200;"

cursor = cnx.cursor()
cursor.execute(GET_TWEETS)

spa_nlp = spacy.load("en_core_web_lg")

for tweet in cursor.fetchall():
	localtwitter.processTweetForNamedEntities(cnx, spa_nlp, tweet)