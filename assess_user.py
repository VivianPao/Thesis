
import twint
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from textblob import TextBlob

ASSESS_LIM_PER_SEARCH = 20

user = "TheEllenShow"
topic = "kind"

def calcTextSentiment(text):
	text = TextBlob(text)
	analysis = text.sentiment.polarity
	return analysis

def calcUserSentiment(listOfStrings):
	sentiment = 0
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
	tweets = collectedData['tweet'].astype(str).tolist()
	return tweets

tweets = getTweetsFrom(user,topic)
userSentiment = calcUserSentiment(tweets)

"""
nodeColor = {}
# Make default colour white somehow... or just iterate through all and make the non-major ones white
if sentiment > -0.1 and sentiment < 0.1:	# If sentiment close to 0, negligible. Neutral outlook
	nodeColor[user].append(white)
elif:
	nodeColor[user].append(green)
else:
	nodeColor[user].append(red)
# Make node edge black
"""


# --> Map to colours!
# 1. Identify how to input colours to draw nodes
# 2. Map the sentiment to node values
# 3. Feed this in and draw on networkx
# 4. Apply for all top 50 users and visualise the network
# 5. Save all the user's tweets into a csv with a file for their name
# 6. Implement for particular dates
# Host online
