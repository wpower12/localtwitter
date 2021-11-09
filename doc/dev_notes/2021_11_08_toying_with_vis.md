# 2021-11-08 Toying with vis

I read a lot, so as a little reward, I'd like to just mess around with creating visualizations of some possible outputs of the database. The first two things that come to mind are;

* Histogram of Hashtag Mention Counts
	- To see how many hashtags are small vs how many are 'viral'
	- I think its power law?
* Word Cloud of Most Popular Hashtags
* Table of most tweeted-from county
	- Or a svg intensity map? chloropleth map?
	- Make it take a particular set of hashtags as input, to filter against?
* Hashtag - County Network Vis
	- Largest single connected component? 
	- Over some threshold? 
	- Would yield data shaped like the reddit project data. "online activity data" per county.
	
If possible, I'd like to parameterize these as much as possible to make it easy to iterate come paper-writing time. It'd be nice to knwo you can recreate images and tables similar to the references you passed on to Srikar today. 


## Working Histogram
This seems to be working on both local and server. Still needs more parameters, like picking start/end dates. I can add that later. 

## Word Cloud
I think this will be the next one to try. I need to go back to reading for a while before I can spend more cycles on this. 