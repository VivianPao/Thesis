
import pandas as pd
import ast
from twitterScraping import *
from Sociogram import *

# ***************************************************************
# CONSTANTS
# ***************************************************************
[IN_CEN,OUT_CEN,EIG_CEN,CLOSE_CEN,BTWN_CEN] = range(0,5)
CENTRALITY = {'in':IN_CEN,'out':OUT_CEN,'eigenvector':EIG_CEN,'closeness':CLOSE_CEN,'betweenness':BTWN_CEN}

# ***************************************************************
# USER INPUTS
# ***************************************************************
reuseData = False
tweetLim = 10000	# Max number of tweets to scrape
topN = 20		# Number of the top influential users to label on visualisation
dates = None

topicList = ['Warrick Lane redevelopment Blacktown','Stage 2 Blacktown Hospital','great northern highway Koodaideri Bridge']
centralityList = ['in','out']

# ***************************************************************
# SCRAPING AND VISUALISATIONS
# ***************************************************************
i = 0
for topic in topicList:
	for centralityType in centralityList:

		collectedData = scrapeTopic(topic,tweetLim,dates)
		if collectedData.empty:
			print('No network for:',topic)
			break

		centralitySelected = CENTRALITY[centralityType]
		mySociogram = Sociogram(collectedData)

		# Create figure and save as image
		f = plt.figure(i)
		i += 1

		plt.axis('off')
		plt.title(topic.title() + ' (' + centralityType + ')',fontweight='bold')
		mySociogram.calcFeatures(topN,centralitySelected)
		mySociogram.drawNetwork()
		f.savefig(topic.title() + ' ' + centralityType + ' sociogram.jpg')

		mySociogram.saveSummary(topic.title() + ' ' + centralityType + ' summary.csv')

