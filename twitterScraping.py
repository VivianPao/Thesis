
import twint
import pandas as pd
from sentimentAnalysis import *

# If the user has been seen before, increment their count. If not, add them into the dictionary and set count to 1.
def addToDict(dictName,keyValue):
	if keyValue not in dictName:
		dictName[keyValue] = 1
	else:
		dictName[keyValue] += 1

# Return dataframe with sentiment analysis and edge + weight dictionary
def organiseData(df):

	df = df[['username','tweet','reply_to']]	# concat string tweets and list of dicts
	df = df.groupby('username',as_index=False).aggregate(sum)	# Group by username (merge duplicates)

	# For each user/ row, rewrite the dictionary. key: mentioned users, val: weight
	# Use the apply() pandas function to create a new row for the dictionary!
	for row in range(len(df)):
		username = df.iloc[row][0]
		listOfDicts = df.iloc[row]['reply_to']

		linkTo = {}	# Create dict, keys as tuples of user -> mentioned user: weight
		for aDict in listOfDicts:
			mentionedUser = aDict['username']
			if mentionedUser != username:
				addToDict(linkTo,(username,mentionedUser))
		df.loc[df.username == username,'reply_to'] = [linkTo]

	# Remove users that have no outgoing connection, i.e. empty dictionary in 'reply_to' column
	df = df.drop(df[df.reply_to == {}].index)
	df['sentiment'] = df['tweet'].apply(calcTextSentiment)	# Add sentiment column

	return df

# Based on the posts of a topic, find all the users that have mentioned a particular person on a topic (or no topic)
def scrapeTopic(topic,tweetLimit):

	c = twint.Config()
	c.Limit = tweetLimit
	c.Pandas = True
	c.Search = topic
	c.Format = "{username} -> {mentions}"
	twint.run.Search(c)

	df = organiseData(twint.storage.panda.Tweets_df)

	return df	# Dataframe of series!

