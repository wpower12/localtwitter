import Util
import twitter
from decouple import config

api = twitter.Api(consumer_key=config('T_CONSUME_KEY'),
				consumer_secret=config('T_CONSUME_SECRET'),
				access_token_key=config('T_ACCESS_KEY'),
				access_token_secret=config('T_ACCESS_SECRET'))

# Using a 'Bucks County' geocode.
# bucks county 40.333625,-75.120857
# philly       39.959715,-75.165765
results = api.GetSearch(geocode="geocode:39.959715,-75.165765,10km", result_type="mixed")

print(results)
for s in results:
	Util.pprintStatus(s)