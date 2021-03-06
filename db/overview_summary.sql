SELECT 
(SELECT COUNT(*) FROM user) as users,
(SELECT COUNT(*) FROM tweet) as tweets,
(SELECT COUNT(*) FROM hashtag) as hashtags,
(SELECT COUNT(*) FROM url) as urls,
(SELECT COUNT(*) FROM county WHERE ignore_county=1) as ignored_counties
(SELECT COUNT(numtweets) FROM
	(SELECT fips, COUNT(*) as 'numtweets' FROM county 
		JOIN tweet ON tweet.countyfips = county.fips
	GROUP BY county.fips) AS countytotals
WHERE numtweets > 100) as 'counties over 100';
