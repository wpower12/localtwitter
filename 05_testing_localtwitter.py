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

areas = [["bucks countyish", "40.333625,-75.120857,5km"],
		 ["philly",          "39.959715,-75.165765,5km"],
		 ["abington",        "40.138342,-75.126028,5km"]]

for name, geocode in areas:
	print("searching {}".format(name))
	num_results = localtwitter.geocodeSearchAndInsert(cnx, api, geocode, report=False, limit=100)
	print("results found {}".format(num_results))
