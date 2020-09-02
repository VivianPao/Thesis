# TO USE THIS CODE:
# Alter parameters in "USER INPUTS" section of this main.py file
# Run "python main.py" from command line

import pandas as pd
import ast
from twitterScraping import *
from Sociogram import *

# ***************************************************************
# USER INPUTS
# ***************************************************************
reuseData = False
topic = "western sydney airport"
tweetLim = 100	# Max number of tweets to scrape
topN = 10		# Number of the top influential users to label on visualisation
centralityType = 'eigenvector'	# Choose from 'in','out','eigenvector','closeness','betweeness'
dates = None

# dates = ['2020-01-01','2020-02-01'] # Dates in form ['YYYY-MM-DD','YYYY-MM-DD']

# ***************************************************************
# CONSTANTS
# ***************************************************************
[IN_CEN,OUT_CEN,EIG_CEN,CLOSE_CEN,BTWN_CEN] = range(0,5)
CENTRALITY = {'in':IN_CEN,'out':OUT_CEN,'eigenvector':EIG_CEN,'closeness':CLOSE_CEN,'betweenness':BTWN_CEN}

# ***************************************************************
# TWITTER SCRAPING
# ***************************************************************
if reuseData == False:
	collectedData = scrapeTopic(topic,tweetLim,dates)
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
centralitySelected = CENTRALITY[centralityType]	# Get correct centrality number code using dictionary

mySociogram = Sociogram(collectedData)

# Create figure and save as image
f = plt.figure()
plt.axis('off')
plt.title(topic.title(),fontweight="bold")
mySociogram.calcFeatures(topN,centralitySelected)
mySociogram.drawNetwork()
f.savefig(topic.title() + " sociogram major.jpg")

mySociogram.saveSummary(topic.title() + 'summary.csv') # (topic +' summary.csv')

