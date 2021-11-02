# 2021-11-01 - URLs and Ready-to-run-at-school

I'd like to make the database schema include any URLs that are found in the entities list for a returned tweet. 

## Mysql schema update
We need a primary key that we can query against based on the text of the url. I think a common practice is to use a hash of the url text as the primary key?

Actually I think this answer is the right idea? SO link [here](https://stackoverflow.com/questions/3735390/best-primary-key-for-storing-urls).
* id
	- primary key
	- automincrement, just a counter to index against?
* urlhash
	- hash of the full url string. 
	- unique and not null
		+ then you search against hash'es.
		+ allows easier insert
	- can use MD5 bc we don't have an agressor?
	- CHAR(32) for value in hex
	- BINARY(16) for value in string of bytes
* url
	- actual string/varchar of the url text.
	- so we can do things to it later, 
		+ split out a base domain
		+ find parameters for api's
		+ might help with named entity detection?

After adding the above, need to test the creation scripts again. 
	
## Working URL Stuff
Ok thats working.

I also took the SQL statements out of the db file and put them in a stand alone file. The imports a wordier, but the code feels nicer.

## Handle Restarts better
I want to add a field to the counties that contains the last tweet id gathered. I THINK I can use that to page the next search and insert?

Yea according to the twitter docs [here](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets) we can use the `since_id` to page. Meaning we get that from the county row, and pass it as a parameter to the general search call. Need to remember how to do the 'last inserted id' stuff in mysql-connector. 

so to do:
* Add last_tweet_id field to the county table. 
* Update search to use that as a parameter
	- `since_id=<last_tweet_id>'
* during search, after each 'succesful' query, need to store the id in the county table. 

Ok so that looks like its working. So this should handle restarts 'gracefully' now. And we wont waste any quieries.

So now the search can be run over and over with increasing size attempts to flesh out the huge counties. 

