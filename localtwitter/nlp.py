from .db import storeNamedEntity, setTweetAsProcessed


def processTweetForNamedEntities(cnx, nlp_parser, tweet):
	t_id, u_id, dtime, t_text, _ = tweet
	tweet_doc = nlp_parser(t_text)
	for ne in tweet_doc.ents:
		storeNamedEntity(cnx, t_id, ne)
	setTweetAsProcessed(cnx, t_id)


def cleanNeString(ne_str):
	ne_str.replace("&", "")