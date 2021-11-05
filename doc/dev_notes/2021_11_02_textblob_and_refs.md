# 2021-11-02 - TextBlob NER and Trying To Track Refs

## Refs
So lesson learned. Locally compiling latex is a pain. I have a texlive install running trying to get my local environment on par with overleafs. Until that works, I'm just going to track references in an online overleaf document [here](https://www.overleaf.com/project/61817965cef7f2375fda1842).

## TextBlob NER
On the suggestion of J, I'm going to try and use TextBlob to do named entity recogntion (NER). 

This is a tool built on top of NLTK that will let me quickly get a list of named entities within each tweet. 

I'd like to make a test script that:
* Pulls a batch of 'unprocessed' tweets
* Runs the full text of each tweet through textblob
* Inserts the found named entities into the DB (if they aren't in there already)
* Associates the tweet with the named entities (another many many link table)

This will require
* Changes to the DB
	- Add a "Named Entities" table
		+ Do we need meta data for them? Maybe?
		+ For now, just a single "entity_name" field that could be unique, and an integer primary key to speed up joins. 
	- Add a "TweetEntities" table for the Tweet<->Entity links.
	- Add a "processed" field to the tweets table to track which tweets have been operated on.
		+ To make it easier to write a 'get me new tweets to work on' query. 
		

