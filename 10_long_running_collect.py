import mysql.connector
import pandas as pd
import tweepy
from decouple import config

import localtwitter

DATABASE_NAME  = "Full_Run_DB_00"

# DB Connection - assumes DATABASE_NAME was created by the db scripts.
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=DATABASE_NAME)

# Twitter API Connection
auth = tweepy.OAuthHandler(config('T_CONSUME_KEY'), config('T_CONSUME_SECRET'))
auth.set_access_token(config('T_ACCESS_KEY'), config('T_ACCESS_SECRET'))
api = tweepy.API(auth)

print("full search and insert.")
localtwitter.resetCountyIgnore(cnx)
for i in [1, 4, 8, 32, 64]:
	print("running full collect; max tweets: {}".format(i*100))
	localtwitter.allCountySearchAndInsert(cnx, api, report=True, limit=100*i, distance="5km")