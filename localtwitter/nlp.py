from .db import storeNamedEntity, setTweetAsProcessed
from .db import getSentimentTweetBatch, insertTweetSentiment
from .db import setSentimentFlag, getTweetCount, resetSentimentFlags

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def processTweetForNamedEntities(cnx, nlp_parser, tweet):
	t_id, u_id, dtime, t_text, _ = tweet
	tweet_doc = nlp_parser(t_text)
	for ne in tweet_doc.ents:
		storeNamedEntity(cnx, t_id, ne)
	setTweetAsProcessed(cnx, t_id)


def analyizeTweetSentiment(cnx, exp_id_str, keywords, batch_size=1000, reset_flags=False):
	if reset_flags:
		resetSentimentFlags(cnx)

	sid = SentimentIntensityAnalyzer()
	i = 0
	total = getTweetCount(cnx)
	while(True):
		tweets = getSentimentTweetBatch(cnx, batch_size)
		if len(tweets) == 0:
			break

		for tweet in tweets:
			found_kws = []
			tweet_id = tweet[0]
			text     = tweet[1] # probably breaks.
			for keyword in keywords:
				# normalize tweet, normalize keyword
				if normalize(keyword) in normalize(text):
					found_kws.append(keyword)

			if(len(found_kws) > 0):
				score = sid.polarity_scores(text)['compound']

				if score > 0:
					score = 1
				elif score < 0:
					score = -1
				else:
					score = 0

				insertTweetSentiment(cnx, exp_id_str, tweet_id, found_kws, score)
			setSentimentFlag(cnx, tweet_id)
			
		i += 1
		print("{}/{}".format(batch_size*i, total))


def normalize(s):
	return s.lower().strip()