import tweepy
import mysql.connector

from decouple import config

import localtwitter

# Twitter API Connection
auth = tweepy.OAuthHandler(config('T_CONSUME_KEY'), config('T_CONSUME_SECRET'))
auth.set_access_token(config('T_ACCESS_KEY'), config('T_ACCESS_SECRET'))

api = tweepy.API(auth)

# DB Connection
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=config('DB_DATABASE'))


localtwitter.allCountySearchAndInsert(cnx, api, report=True, limit=200, distance="5km")