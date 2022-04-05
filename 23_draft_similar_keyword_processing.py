import spacy

TOPIC_KEYWORD_FN = "data/tweet_keywords.csv"
SIMILAR_KEYWORDS_FN = "data/keywords_with_similars.csv"

keywords = []
with open(TOPIC_KEYWORD_FN, 'r') as f:
	for line in f.readlines():
		keywords.append(line.split(" ")[0])

nlp = spacy.load('en_core_web_lg')

# Document Objects for Each Keyword
kw_docs = {}
for keyword in keywords:
	kw_docs[keyword] = nlp(keyword)

# Set of similarity scores between each keyword and each token
kw_similars = {}
for token in nlp.vocab:
	if(token.has_vector and token.is_lower and token.is_alpha):
		for keyword in keywords:
			if keyword not in kw_similars:
				kw_similars[keyword] = []

			kw_similars[keyword].append((token.text, kw_docs[keyword].similarity(token)))

# Sorting the similarity scores for each token for each keyword
for keyword in keywords:
	sorted_kw_tokens = sorted(kw_similars[keyword], key=lambda ts: -ts[1])
	kw_similars[keyword] = sorted_kw_tokens[:5] # Top 5 similar words for each
	print(keyword, kw_similars[keyword])


# OOF ok misunderstood what was in the nlp.vocab thing. 
# I think it keeps a running tally of all the things added to it? Idk.
# that is, NLP builds up a vocab based on all the strings added to it?
# so when i iterate over vocab, I'm just iterating over all the 
# tokens its seen so far. Meh. MIGHT be useful to find other keywords
# but I think I can settle for lemmatizing the keywords, lemmatizing
# the tweet text, and searching that way. 

# So yea, this happens at the same time as searching will. 