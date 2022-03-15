import spacy

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from csv import reader

TOPIC_KEYWORD_FN = "data/tweet_keywords.csv"
TWEET_FN = "data/full_tweets_2022_02_24.csv"
OUTPUT_KWS_FN   = "data/full_tweets_2022_02_24_KEYWORDS.csv"

nlp = spacy.load('en_core_web_lg')
sid = SentimentIntensityAnalyzer()

lemma_keywords = []
with open(TOPIC_KEYWORD_FN, 'r') as f:
	for line in f.readlines():
		raw_kw = line.split(" ")[0]
		lemma_keywords.append(nlp(raw_kw)[0].lemma_)


def spacyProcessedTokens(text):
	tokens = nlp(text)
	# Lemmatize each token
	# From https://towardsdatascience.com/complete-guide-to-perform-classification-of-tweets-with-spacy-e550ee92ca79
	tokens = [word.lemma_.lower().strip() if word.lemma_ != "PROPN" else word.lower_ for word in tokens]
	return tokens


with open(TWEET_FN, 'r') as in_f, open(OUTPUT_KWS_FN, 'w') as out_f:
	in_f.readline() # Skip column row. 
	
	# Use a csv.reader to avoid issues with commas in tweet text.
	# CSV columns: tweetid, date, fips, text
	for line in reader(in_f):
		tweet_id = line[0]
		date     = line[1]
		fips     = line[2]
		text     = line[3]

		found_kws = []
		text_tokens = spacyProcessedTokens(text)
		for kw in lemma_keywords:
			if kw in text_tokens:
				found_kws.append(kw)
		
		# Get sentiment
		score = sid.polarity_scores(text)['compound']

		# Build result row string:
		# (tweetid, sent_score, list-of-found-kws)
		row_str = "{}, {}, ".format(tweet_id, score)

		# If any are found, save out tweet and list of kws
		if(len(found_kws) > 0):
			row_str += ", ".join(found_kws)
		else:
			row_str = row_str[:-2] # remove trailing comma.

		row_str += "\n"
		out_f.write(row_str)
