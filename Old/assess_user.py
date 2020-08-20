
import twint
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from textblob import TextBlob

# Maximum number of tweets we'll use to calculate the user's overall sentiment
ASSESS_LIM_PER_SEARCH = 20

# FLAGS:
# SAVE_TO_TEXT = True

def calcTextSentiment(text):
	text = TextBlob(text)
	analysis = text.sentiment.polarity
	return analysis

def calcUserSentiment(listOfStrings):
	sentiment = 0	# Initial sentiment of 0
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

	collectedData = twint.storage.panda.Tweets_df	# Dataframe of series!
	if collectedData.empty == False:
		tweets = collectedData['tweet'].astype(str).tolist()
	else:	# If there wasn't any data, return an empty list
		tweets  = []

	# WRITE LIST TO A TEXT FILE. VARIABLE FILE NAME
	with open(user+'.txt', 'w') as f:
	    for item in tweets:
	        f.write("%s\n" % item)

	return tweets

# Example of usage
if __name__ == "__main__":
	user = "TheEllenShow"
	topic = "kindness"
	tweets = getTweetsFrom(user,topic)
	userSentiment = calcUserSentiment(tweets)
