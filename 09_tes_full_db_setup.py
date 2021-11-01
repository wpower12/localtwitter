import mysql.connector
import pandas as pd
import tweepy
from decouple import config

import localtwitter

DATABASE_NAME  = "TEST_14"
COUNTY_INFO_FN = "data/us-county-data.csv"

# DB Connection
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'))

localtwitter.createSchema(cnx, DATABASE_NAME)
localtwitter.populateCountyTable(cnx, pd.read_csv(COUNTY_INFO_FN, dtype={'FIPS': str}))

print("testing search and insert.")
# Twitter API Connection
auth = tweepy.OAuthHandler(config('T_CONSUME_KEY'), config('T_CONSUME_SECRET'))
auth.set_access_token(config('T_ACCESS_KEY'), config('T_ACCESS_SECRET'))
api = tweepy.API(auth)

localtwitter.allCountySearchAndInsert(cnx, api, report=True, limit=100, distance="5km")