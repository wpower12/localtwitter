import mysql.connector
import pandas as pd
import tweepy
from decouple import config

import localtwitter

DATABASE_NAME  = "Full_Run_DB_00"
COUNTY_INFO_FN = "data/us-county-data.csv"

# DB Connection
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'))

# have to change this on the school server. forgot what the version theres is. 
localtwitter.createSchema(cnx, DATABASE_NAME, encoding="utf8mb4_0900_ai_ci")
localtwitter.populateCountyTable(cnx, pd.read_csv(COUNTY_INFO_FN, dtype={'FIPS': str}))

print("search and insert.")

# Twitter API Connection
auth = tweepy.OAuthHandler(config('T_CONSUME_KEY'), config('T_CONSUME_SECRET'))
auth.set_access_token(config('T_ACCESS_KEY'), config('T_ACCESS_SECRET'))
api = tweepy.API(auth)


for i in range(1, 5):
	print("running full collect, iteration: {}".format(i))
	localtwitter.allCountySearchAndInsert(cnx, api, report=True, limit=100*i, distance="5km")