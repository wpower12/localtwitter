from urllib.request import urlopen
import json 
import pandas as pd
import plotly.express as px
import math
import numpy as np

COUNTY_JSON_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'
TWEET_COUNTS_FN = 'data/tweet_counts_by_county.csv'
UNIQUE_HASH_COUNTS_FN = 'data/unique_hashtag_counts_by_county.csv'

with urlopen(COUNTY_JSON_URL) as response:
	counties = json.load(response)

# Tweet Counts
df_tweets = pd.read_csv(TWEET_COUNTS_FN, dtype={'countyfips': str})
df_tweets['tweets']    = df_tweets['COUNT(*)'].astype(str) 
df_tweets['logtweets'] = np.log(df_tweets['COUNT(*)']+1)
fig_tweets = px.choropleth(df_tweets, 
	geojson=counties, 
	locations='countyfips',
	color="logtweets",
	color_continuous_scale="Viridis",
	range_color=(0, df_tweets['logtweets'].max()),
	scope="usa",
	labels={'logtweets':'Log(# Tweets)'})

fig_tweets.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig_tweets.show()

# Unique Hashtag Counts
df_hashes = pd.read_csv(UNIQUE_HASH_COUNTS_FN, dtype={'countyfips': str})
df_hashes['logcount'] = np.log(df_hashes['COUNT(DISTINCT tweethashtags.hashtag)']+1)
fig_hashes = px.choropleth(df_hashes, 
	geojson=counties, 
	locations='countyfips',
	color="logcount",
	color_continuous_scale="Viridis",
	range_color=(0, df_hashes['logcount'].max()),
	scope="usa",
	labels={'logcount':'Log(# Unique Hashtags)'})

fig_hashes.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig_hashes.show()