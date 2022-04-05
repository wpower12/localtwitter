import requests
from bs4 import BeautifulSoup as bs

SEED_TAGS = ["republicans", "liberals", "bachelor"]
OUTPUT_FN = "data/test_scrape_related.csv"


def findRelatedHashtags(hashtag):
	SEARCH_URL = "https://best-hashtags.com/hashtag/{}/"
	page = requests.get(SEARCH_URL.format(hashtag))
	soup = bs(page.content, "html.parser")

	# As of 2022-03-29 - Hashtag lists are always in two 
	# custom tags; <p1> and <p2>. The soup parser seems to 
	# not care that they aren't in the html spec? 
	top_1 = soup.find_all("p1")[0]
	top_2 = soup.find_all("p2")[0]
	
	hashtags = set()
	for d in [top_1, top_2]:
		for ht in d.text.replace("#", "").split(" "):
			if(ht != ""): # Yuck. 
				hashtags.add(ht)
	return hashtags


results = dict()
for seed_ht in SEED_TAGS:
	for ht in findRelatedHashtags(seed_ht):
		if(ht in results):
			results[ht].append(seed_ht)
		else:
			results[ht] = [seed_ht]

with open(OUTPUT_FN, 'w') as out_f:
	for k in results:
		out_str = "{}, ".format(k)
		out_str += ", ".join(results[k]).replace("'", "")
		out_str += "\n"
		out_f.write(out_str)