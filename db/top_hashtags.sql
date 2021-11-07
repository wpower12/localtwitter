SELECT text, COUNT(*) FROM hashtag as ht
JOIN tweethashtags as tht on ht.text=tht.hashtag
GROUP BY text
ORDER BY COUNT(*) DESC
LIMIT 100;