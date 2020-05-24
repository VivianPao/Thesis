# @KusanagiMizuho
# spoilliest --> Fan account
# Explaining how to use Twint: https://medium.com/@erika.dauria/scraping-tweets-off-twitter-with-twint-a7e9d78415bf
# Create sociogram of people associated with/ mentioning the main account
# Create a CSV file that can be put into Gephi
# --> Rewatch Gephi tutorials

# Find all connections related to this user about this topic... additional
# mentions and mentioned by
# follows and followed by
# likes and liked by
# retweets and retweeted by
# ??? --> But if you do both directions, you'll get doubles ups. Better to do one way only.

# https://github.com/twintproject/twint/wiki

import twint
import pandas as pd
import numpy as np

TWEET_LIM_PER_SEARCH = 10

# THESE ARE ALL USER CENTRIC ATM!
# Change later so that the returned dataframes also show the centric user in a column
# Then you can stack the dataframes for the final output

# Based on the posts of a topic, find all the users that have mentioned a particular person on a topic (or no topic)
def findMentioners(username,topic):

	# Initialisation with the topic
	c = twint.Config()
	c.Limit = TWEET_LIM_PER_SEARCH
	c.Pandas = True

	c.Search = topic
	c.To = username	# A Reply to a user or mention of them. Counts as a 'mention' anyway
	c.Format = "{mentions} | {username}"
	twint.run.Search(c)

	collectedData = twint.storage.panda.Tweets_df	# Dataframe of series!
	splicedData = collectedData.loc[:,('username')]	# Why does this gives us a series instead of a dataframe?
	splicedData = splicedData.to_frame()			# Turn it into a dataframe
	splicedData = splicedData.rename(columns={'username': 'Source'}) # Rename the column
	targetData = [username] * len(splicedData.index)
	splicedData['Target'] = targetData

	return splicedData

# Find all the followers of the user
# Fairly different to findMentioners because open source code gives things in inconsistent dataformats
def findFollowers(username):

	c = twint.Config()
	c.Limit = TWEET_LIM_PER_SEARCH
	c.Pandas = True
	c.Username = username
	twint.run.Followers(c)

	collectedData = twint.storage.panda.Follow_df	# Dataframe of dataframes!
	splicedData = collectedData.loc[:,('followers')][username]	# Gives an array
	targetData = [username] * len(splicedData)
	finalData = pd.DataFrame({'Source': splicedData,'Target': targetData})

	return finalData

# Add a new column of weights
def prepareForSociogram(listOfDFs):
	finalData = pd.concat(listOfDFs,ignore_index = True)
	finalData['Link'] = [1] * len(finalData.index)
	return finalData


userOfInterest = "KusanagiMizuho"
mentioners = findMentioners(userOfInterest,"")
followers = findFollowers(userOfInterest)
finalTable = prepareForSociogram([mentioners,followers])
finalTable.to_csv("sociogramCSV.csv",index = False)
print(finalTable)


