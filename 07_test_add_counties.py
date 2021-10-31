import mysql.connector
import pandas as pd
from decouple import config

import localtwitter

# DB Connection
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=config('DB_DATABASE'))

COUNTY_INFO_FN = "data/us-county-data.csv"
county_df = pd.read_csv(COUNTY_INFO_FN, dtype={'FIPS': str})

localtwitter.populateCountyTable(cnx, county_df)