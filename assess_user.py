
import twint
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from textblob import TextBlob

ASSESS_LIM_PER_SEARCH = 5

def calcTextSentiment(text):
	text = TextBlob(text)
	analysis = text.sentiment.polarity
	return analysis

def calcUserSentiment(listOfStrings):
	sentiment = 0

	if len(listOfStrings) == 0:
		return sentiment
	else:
		# Calculate individual string sentiment and then get the average
		for string in listOfStrings:
			sentiment += calcTextSentiment(string)
		sentiment /= len(listOfStrings)
		return sentiment

def getTweetsFrom(user,topic):
	# Warning, Twint is VERY slow when getting tweets from specific users
	c = twint.Config()
	c.Limit = ASSESS_LIM_PER_SEARCH
	c.Pandas = True
	c.Username = user
	c.Format = "{username} | {tweet}"
	c.Search = topic
	twint.run.Search(c)

	# May come back blank...
	collectedData = twint.storage.panda.Tweets_df	# Dataframe of series!
	if collectedData.empty == False:
		tweets = collectedData['tweet'].astype(str).tolist()
	else:
		tweets  = []

	# WRITE LIST TO A TEXT FILE. VARIABLE FILE NAME
	with open(user+'.txt', 'w') as f:
	    for item in tweets:
	        f.write("%s\n" % item)

	return tweets

if __name__ == "__main__":
	user = "JAPANFESS"
	topic = "akatsuki no yona"
	tweets = getTweetsFrom(user,topic)
	userSentiment = calcUserSentiment(tweets)


# --> Map to colours!
# 1. Identify how to input colours to draw nodes
# 2. Map the sentiment to node values
# 3. Feed this in and draw on networkx
# 4. Apply for all top 50 users and visualise the network
# 5. Save all the user's tweets into a csv with a file for their name
# 6. Implement for particular dates
# Host online
