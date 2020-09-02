 
import pandas as pd
import ast

from twitterScraping import *
from Sociogram import *

# ***************************************************************
# USER INPUTS
# ***************************************************************
TOPIC = "western sydney airport"
TWEET_LIM = 100				# The number of tweets to scrape from Twitter before stopping.
TOP_N = 10					# How many major users to identify. If TOP_N = 10, code names top 10 users.

REUSE_DATA = False

# ***************************************************************
# TWITTER SCRAPING
# ***************************************************************

if REUSE_DATA == False:
	collectedData = scrapeTopic(TOPIC,TWEET_LIM)
	collectedData.to_csv('data.csv',index=False)
else:
	collectedData = pd.read_csv('data.csv')
	weightedLinks = collectedData['reply_to'].tolist()	# Link of dictionaries
	columnIndex = collectedData.columns.get_loc('reply_to')
	for i in range(len(weightedLinks)):		# Reading in the dictionaries from string format
		collectedData.iloc[i,columnIndex] = [ast.literal_eval(weightedLinks[i])]	# [i]['reply_to'] is a COPY. need to reference properly!

# ***************************************************************
# VISUALISATION
# ***************************************************************

mySociogram = Sociogram(collectedData)
mySociogram.drawNetwork(TOP_N)
mySociogram.saveSummary(TOPIC +' summary.csv')

# TO DO:
# - Remove overlapping, get better layout
# - Add time frame in which to scrape data: since and until
# - Fix sentiment analysis
# - Add option to select type of centrality used to identify influential users
