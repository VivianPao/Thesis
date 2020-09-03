
import pandas as pd
import ast
from twitterScraping import *
from Sociogram import *

# ***************************************************************
# CONSTANTS
# ***************************************************************
[IN_DEG_CEN,OUT_DEG_CEN,DEG_CEN,EIG_CEN,CLOSE_CEN,BTWN_CEN] = range(0,6)
CENTRALITY = {'in degree':IN_DEG_CEN,'out degree':OUT_DEG_CEN,'degree':DEG_CEN,'eigenvector':EIG_CEN,'closeness':CLOSE_CEN,'betweenness':BTWN_CEN}

# ***************************************************************
# USER INPUTS
# ***************************************************************
reuseData = False
tweetLim = 1000#10000
topN = 20
dates = None

topic = 'covid' # Or list of topics ['chicken','beef']
centralityList = 'degree' # Or List ['degree','betweenness']

# ***************************************************************
# SCRAPING AND VISUALISATIONS
# ***************************************************************
i = 0
for currTopic in topic:
	for centralityType in centralityList:

		collectedData = scrapeTopic(currTopic,tweetLim,dates)
		if collectedData.empty:
			print('No network for:',currTopic)
			break

		centralitySelected = CENTRALITY[centralityType]
		mySociogram = Sociogram(collectedData)

		# Create figure and save as image
		f = plt.figure(i,figsize=[10, 8])
		i += 1

		plt.axis('off')
		plt.title(currTopic.title() + ' (' + centralityType + ')',fontweight='bold')
		mySociogram.calcFeatures(topN,centralitySelected)
		mySociogram.drawNetwork()
		plt.tight_layout()
		f.savefig(currTopic.title() + ' ' + centralityType + ' sociogram.jpg')

		mySociogram.saveSummary(currTopic.title() + ' ' + centralityType + ' summary.csv')

input("Press Enter to close all plots...")

