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
import time

TWEET_LIM_PER_SEARCH = 100
FROM = 0
TO = 1
SLEEP_TIME = 5

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
	c.Format = "{username} | {mentions}"
	twint.run.Search(c)

	collectedData = twint.storage.panda.Tweets_df	# Dataframe of series!
	sourceData = collectedData.loc[:,('username')]	# Why does this gives us a series instead of a dataframe?
	sourceData = sourceData.to_frame()			# Turn it into a dataframe
	sourceData = sourceData.rename(columns={'username': 'Source'}) # Rename the column
	targetData = [username] * len(sourceData.index)
	sourceData['Target'] = targetData

	return sourceData

# USER CENTRIC search of who they talk about
def findMentioning(username,topic):

	# Initialisation with the topic
	c = twint.Config()
	c.Limit = TWEET_LIM_PER_SEARCH
	c.Pandas = True
	c.Username = username
	c.Search = topic
	c.Format = "{username} | {mentions}"
	twint.run.Search(c)

	collectedData = twint.storage.panda.Tweets_df	# Dataframe of series!
	mentions = collectedData.loc[:,('reply_to')]

	mentionsArray = []

	for row in range(len(mentions)):
		currentUser = mentions[row][FROM]['username']
		for nthMention in range(TO,len(mentions[row])):	# For each mentioned user, create a new link to the poster
			mentionsArray.append([currentUser,mentions[row][nthMention]['username']])

	sourceData = [row[FROM] for row in mentionsArray]	# Create new array from the 1st column
	targetData = [row[TO] for row in mentionsArray]		# Create new array from the 2nd column
	finalData = pd.DataFrame({'Source': sourceData,'Target': targetData})

	return finalData

# Find all the followers of the user
# Fairly different to findMentioners because open source code gives things in inconsistent dataformats
def findFollowers(username):

	c = twint.Config()
	c.Limit = TWEET_LIM_PER_SEARCH
	c.Pandas = True
	c.Username = username
	twint.run.Followers(c)

	collectedData = twint.storage.panda.Follow_df	# Dataframe of dataframes!
	sourceData = collectedData.loc[:,('followers')][username]	# Gives an array
	targetData = [username] * len(sourceData)
	finalData = pd.DataFrame({'Source': sourceData,'Target': targetData})

	return finalData

def findFollowing(username):

	c = twint.Config()
	c.Limit = TWEET_LIM_PER_SEARCH
	c.Pandas = True
	c.Username = username
	twint.run.Following(c)

	collectedData = twint.storage.panda.Follow_df	# Dataframe of dataframes!
	targetData = collectedData.loc[:,('following')][username]	# Gives an array
	sourceData = [username] * len(targetData)
	finalData = pd.DataFrame({'Source': sourceData,'Target': targetData})
	# print(finalData)
	return finalData

# Add a new column of weights
def prepareForSociogram(listOfDFs):
	finalData = pd.concat(listOfDFs,ignore_index = True)
	finalData['Link'] = [1] * len(finalData.index)
	return finalData

# Error when Twitter stops you from scraping:
# CRITICAL:root:twint.feed:Follow:IndexError
# Have delays

userOfInterest = "nowestconnex"

mentioners = findMentioners(userOfInterest,"")
time.sleep(SLEEP_TIME)
# followers = findFollowers(userOfInterest)
# time.sleep(SLEEP_TIME)
# following = findFollowing(userOfInterest)
# time.sleep(SLEEP_TIME)
mentioning = findMentioning(userOfInterest,"")

# Deal with case sensitivity soon!

finalTable = prepareForSociogram([mentioners,mentioning])#,followers,following])
# finalTable = finalTable.str.lower()
finalTable.to_csv("sociogramCSV.csv",index = False)
print(finalTable)


