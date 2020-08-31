
import twint
import pandas as pd
import numpy as np

# If the user has been seen before, increment their count. If not, add them into the dictionary and set count to 1.
def __addToDict__(dictName,keyValue):
	if keyValue not in dictName:
		dictName[keyValue] = 1
	else:
		dictName[keyValue] += 1

# Based on the posts of a topic, find all the users that have mentioned a particular person on a topic (or no topic)
def scrapeTopic(topic,tweetLimit):

	c = twint.Config()
	c.Limit = tweetLimit
	c.Pandas = True
	c.Search = topic
	c.Format = "{username} -> {mentions}"
	twint.run.Search(c)

	return twint.storage.panda.Tweets_df	# Dataframe of series!

# I: dataframe, O: dict
def organiseData(df):

	# concat string tweets and list of dicts
	df = df[['username','tweet','reply_to']]
	df = df.groupby('username').aggregate(sum)

	# For each user/ row, rewrite the dictionary. key: mentioned users, val: weight
	for row in range(len(df)):
		username = df.iloc[row][0]
		listOfDicts = df.iloc[row]['reply_to']

		linkTo = dict()	# Create dict to store names of mentioned users
		for aDict in listOfDicts:
			mentionedUser = aDict['username']
			if mentionedUser != username:
				__addToDict__(linkTo,mentionedUser)
		df.iloc[row]['reply_to'] = [linkTo]

	return df

# df = scrapeTopic("chicken",100)
# df = organiseData(df)


