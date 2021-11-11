import pandas as pd
import numpy  as np
import wordcloud
import matplotlib.pyplot as plt

from .sql import GET_HASHTAG_MENTIONCOUNT_HIST, GET_HASHTAG_FREQ


def createHashtagMentionCountHistogram(cnx, log=False, fn=None, max_mentions=500):
	cursor = cnx.cursor()
	cursor.execute(GET_HASHTAG_MENTIONCOUNT_HIST)

	htmc_df = pd.DataFrame(cursor.fetchall())
	print(htmc_df.head())
	max_mention = htmc_df[0].max()

	y = np.zeros((max_mentions))
	for row in htmc_df.iterrows():
		x_id = row[1][0]
		if(x_id < MAX_MENTION):
			y[x_id] = row[1][1]

	if log:
		y = np.log(y)
		y[y == -np.inf] = 0

	fig, ax = plt.subplots()
	ax.bar(range(max_mentions), height=y)

	plt.title("Hashtag Mention Count Histogram")
	plt.ylabel("# Hashtags")
	plt.xlabel("# Mentions")

	if fn != None:
		plt.savefig(fn)

	plt.show()


def createHashtagWordCloud(cnx, fn=None, county_list=None):
	# I think I'd like it to be parameterized by WHERE'ing on counties, if provided,
	# as well as a limit count. That means making the SQL parameterized. 
	cursor = cnx.cursor()
	cursor.execute(GET_HASHTAG_FREQ)

	text_f_dict = {}
	for res in cursor.fetchall():
		text_f_dict[res[0]] = res[1]

	wc = wordcloud.WordCloud(background_color="white", max_words=500)
	wc.generate_from_frequencies(text_f_dict)

	plt.imshow(wc)
	plt.axis("off")

	if fn != None:
		plt.savefig(fn)

	plt.show()