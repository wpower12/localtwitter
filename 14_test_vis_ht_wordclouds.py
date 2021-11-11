import mysql.connector
from decouple import config

import localtwitter

DATABASE_NAME = "Full_Run_DB_00"

cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=DATABASE_NAME)

localtwitter.createHashtagWordCloud(cnx, fn="test.png")