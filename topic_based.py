
import twint
import pandas as pd
import numpy as np

TWEET_LIM_PER_SEARCH = 500
FROM = 0
TO = 1

## TOPIC-CENTRIC

def prepareForSociogram(listOfDFs):
	finalData = pd.concat(listOfDFs,ignore_index = True)
	finalData['Link'] = [1] * len(finalData.index)
	return finalData

# Based on the posts of a topic, find all the users that have mentioned a particular person on a topic (or no topic)
def findMentioning(topic):

	# Initialisation with the topic
	c = twint.Config()
	c.Limit = TWEET_LIM_PER_SEARCH
	c.Pandas = True
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

mention = findMentioning("westconnex")#"akatsuki no yona")
finalTable = prepareForSociogram([mention])
finalTable.to_csv("sociogramCSV.csv",index = False)
print(finalTable)