# 2021-11-05 Working on NER. Server Run Issues

## NER
So far I think I have a working method for processing a tweet. You pass in a connection to the db, an nlp parser, and the tweet. This also sets the tweet to processed. 

Of note; it checks to see if there is a unique NE first, and if so, recovers its id. THEN it inserts. This was needed because I was worried about using the name of the named entity as the actual key, because they can be long? Now its just a simple int as a PK/FK. 

Next steps would be cleaning it up so its easier to use in a 'full script'. But I think its basically there.

This required adding to the database.

## Database Changes
Now have the `namedentity` and `namedentities` tables in the DB with their corresponding FK's. The create scripts have been updated. I should test them, and then regenerate the DB schema image for the README file. 


## Server Issues
So the long term run hit a snag, and I had to wrap the full geo searches in a try catch block. I think the biggest source of random exceptions wont be my going over the rate limit, but for when there are issues with the internet connection itself. The specific exception mentioned was a 'HTTPConnectionPool' exception. Right now I handle this by just waiting 15 minutes and trying again.  


## Other Goals/Next Steps
Stop words? Better reconnection handling? 