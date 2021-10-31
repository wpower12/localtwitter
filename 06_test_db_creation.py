import mysql.connector
from decouple import config

import localtwitter

# DB Connection
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'))

localtwitter.createSchema(cnx, 'TEST_DB_00')