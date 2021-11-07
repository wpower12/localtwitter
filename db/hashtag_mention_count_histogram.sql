SELECT num_mentions, COUNT(*)
FROM 
	(SELECT text, COUNT(*) as 'num_mentions' FROM hashtag as ht
	JOIN tweethashtags as tht on ht.text=tht.hashtag
	GROUP BY text) as T1
GROUP BY num_mentions
ORDER BY num_mentions ASC;
