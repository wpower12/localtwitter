# 2021-10-30 - Including hashtags and URLs Scrape

## Adding Hashtags First
Will require:
* Creating new tables
	- hashtag
		+ meta for a single hashtag
		+ will use the hashtag text as the primary key
	- tweethashtags
		+ many-to-one link between tweets and hashtags
* Updating the `insertTweet` method to push any found hashtags.
	- Just need to open a response back up to make sure you can read the returned model right.

This could be duplicated, with 'urls', 'tweetsurls' tables. But just hashtags for now seems good. 

## Stretch Goals
After thats working, stretch goals:

* Make `createDatabase` script and test it
	- Make it take a `database_name` parameter, so we can generalize away from the hard coded value of `localized_twitter`.
	- Will mean updating the `insertTweet` method to take a `database_name` parameter as well.
	- Will greatly ease testing the `createTables` method.
		+ Note - **So this should be done first!!!**
* Creating/planning out a `parseLocationsWithGeoApi` method
	- For automating the process of trying to resolve the location field in the user table with an actual address, and then county-fips code. 
	- Should be built to run apart from other scripts, operating over an already filled in database of users.
	- Will need SQL for 
		+ obtaining lists of users who have not been processed
		+ Inserting found addresses and fips-codes for users after they've been processed by the geoapi request handler.
		

## New Tables and SQL
Just gonna do these hand in hand. 

Ok to get entity data out of a tweet model, we have to use a dict, not dots. 

So we write `tweet.entities['hashtags']` to get a list of hashtags. Each hashtag is also a dict, with the `hashtag['text'` field giving you the actual text of the hashtag. 

## Working insert
Ok so thats working. The `05` test script is running, and I see in the workbench that hashtags and tweethashtags being put into the database. 

Moving onto the new database name parameter.

## Database Name Parameter
Again, will have to change the insert script.

I THINK I can actually leave out the database name and leave it up to the cursor? I'm going to try that really quick. 

Then the only time we use the database name from the config file is right up front when we generate the connection object. 

Yup! that worked. Nice. 

So I think that means the 'create table' method can just not write it out either. We are passing in a connection object that already knows its working on the `<DATABASE NAME>`database. So tables will go there. 

## Create Tables Methods
I want to do this in a 'packagable' way. Idk if that means just like, inlining all the sql? Is it ok to open an SQL file in python and use that over the connector? idk. 

To start, I think I'll just inline it all? Right now this is just for me. If I ever made it for other people I'd have to somehow make it "connector agnostic".

Ok this is working. Commited a new db script that has a tidy create method. Ended up inlining sql, but in a way that mirrored the examples from the connector documentation. 

## County Data
I'd like to get the county data into the database. 

Found a nice data file from 'opendatasoft' [here](https://public.opendatasoft.com/explore/dataset/us-county-boundaries/table/?disjunctive.statefp&disjunctive.countyfp&disjunctive.name&disjunctive.namelsad&disjunctive.stusab&disjunctive.state_name) that has the lat/long of the centroid of each us county. I opened its raw and pared it down to a csv of just what I need, by county FIPS code. Thats in the data directory now. Creating a script that reads that and fills in a county table.

Need to add a county table to the database, and then add its insert code into the db list.

Ok I have the county data in the database now, and its create sql is added to the create method. 

Now to make a query that runs over all the counties in the db.

## Full County Gather
Ok so I think I have a working full county gather. Just taking 5 seconds per county to get a single 100 query will take 4.5 hours. So a 'full run' with 2 queries per could take up to 9. Probably somewhere in between. I'll leave it running over night and see what happens. 

I added a few things to the database. Notably, the user table now has a forgein key to the county tabke through a `countyfips` field. 

Gah, really hoping this doesn't except out due to a rate limit. I'm hoping I was robust enough. Eventually I need to figure out using the API to poll if I'm limited or not, so I could handle waiting out a window before retrying. so far so good. almost 2k tweets gathered while i wrote this section. 


