 
import pandas as pd
import ast

from twitterScraping import *
from Sociogram import *

# ***************************************************************
# USER INPUTS
# ***************************************************************
TOPIC = "western sydney airport"
TWEET_LIM = 100
TOP_N = 10

REUSE_DATA = False

# ***************************************************************
# TWITTER SCRAPING
# ***************************************************************
if REUSE_DATA == False:
	collectedData = scrapeTopic(TOPIC,TWEET_LIM)
	collectedData.to_csv('data.csv',index=False)
else:	# Dicts by default in string format. Rewrite the column with real dicts.
	collectedData = pd.read_csv('data.csv')
	weightedLinks = collectedData['reply_to'].tolist()	# List of dicts
	columnIndex = collectedData.columns.get_loc('reply_to')
	for i in range(len(weightedLinks)):		
		collectedData.iloc[i,columnIndex] = [ast.literal_eval(weightedLinks[i])]

# ***************************************************************
# VISUALISATION
# ***************************************************************
mySociogram = Sociogram(collectedData)
mySociogram.drawNetwork(TOP_N)
mySociogram.saveSummary('summary.csv') # (TOPIC +' summary.csv')




# TO DO:
# - Remove overlapping, get better layout
# - Add time frame in which to scrape data: since and until
# - Fix sentiment analysis
# - Add option to select type of centrality used to identify influential users
