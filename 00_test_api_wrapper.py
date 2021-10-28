import twitter
from decouple import config

api = twitter.Api(consumer_key=config('T_CONSUME_KEY'),
				consumer_secret=config('T_CONSUME_SECRET'),
				access_token_key=config('T_ACCESS_KEY'),
				access_token_secret=config('T_ACCESS_SECRET'))

# Uses the general search for twitter. 
results = api.GetSearch(raw_query="q=twitter%20&result_type=recent&count=10")

print(results)