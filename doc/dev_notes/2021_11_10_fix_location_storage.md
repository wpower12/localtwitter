# 2021-11-10 Fix location storage

So I realized I'm doing the location storage wrong. I need to track the location of the tweet as well. The tweet is the thing being associated with the geocode query, not the user. A user can set their location to anything, and then tweet from anywhere. If they have the location services on, the lat long of their current location will be applied to the tweet (in general, I think. Idk. but its less wrong than what I'm currently assuming).

So I need to change a few things:

* db
	- data for user and tweet will change
	- tweet
		+ store location from returned tweet object
		+ Need to check where we get that from the object, I think its the 'geo' field. 
		+ store censusfips of the county whose query is being ran. 
	- user
		+ don't store a geocode.
		+ I think thats it? already storing the user location string. 
	- Schema
		+ add countyfips to the tweet table
		+ remove countyfips from user table
		+ create fk from tweet.countyfips to county.fips
		+ remove fk from user.countyfips to county.fips
		+ add lat/long fields to tweet table?
			* Might need to just make a geofield?
			* so if there is a specific lat/long for the tweet, we'd make geo string
			* no lets do lat long
			* if theres not lat/long in the geo object for the tweet, get the latlong from the geocode that's being used. 
			* Otherwise store the lat/long from the geo field. 
			* I think that lets us do easier geo comparisons later? 
* sql
	- new SQL to match changes to
		+ tweet
		+ user
	- update create table and fk SQL
		+ tweet
		+ user
		
## location, coordinates, places
So it looks like most of these are null? blarg. 

I'm gonna set up the inserts to work, and ill allow nulls for lat/long. Won't insert them but ill keep the fields. 

Then I'll let it run a while and try to print out all of the above fields to see how often we'll get a lat long, and how we can handle its insert properly. 

Ok so i think it's working. I'll need to update it to pull lat/long if it exists, but for now it's at least associating hashtags with counties properly. That is, its connecting a fips to a tweet, and then a hashtag to a tweet.

