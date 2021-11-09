import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt


from .sql import GET_HASHTAG_MENTIONCOUNT_HIST


def createHashtagMentionCountHistogram(cnx, log=False, fn=None):
	cursor = cnx.cursor()
	cursor.execute(GET_HASHTAG_MENTIONCOUNT_HIST)

	htmc_df = pd.DataFrame(cursor.fetchall())
	max_mention = htmc_df[0].max()

	y = np.zeros((max_mention+1))
	for row in htmc_df.iterrows():
		x_id = row[1][0]
		y[x_id] = row[1][1]

	if log:
		y = np.log(y)

	fig, ax = plt.subplots()
	ax.bar(range(max_mention+1), height=y)

	plt.title("Hashtag Mention Count Histogram")
	plt.ylabel("# Hashtags")
	plt.xlabel("# Mentions")

	if fn != None:
		plt.savefig(fn)

	plt.show()
