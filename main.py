# TO USE THIS CODE:
# Alter parameters in "USER INPUTS" section of this main.py file
# Run "python main.py" from command line

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
tweetLim = 1000	# Max number of tweets to scrape

topic = "fruits basket"
topN = 10		# Number of the top influential users to label on visualisation
centralityType = 'degree'	# Choose from 'in degree','out degree','degree','eigenvector','closeness','betweeness'
dates = None

# dates = ['2020-01-01','2020-02-01'] # Dates in form ['YYYY-MM-DD','YYYY-MM-DD']

# ***************************************************************
# TWITTER SCRAPING
# ***************************************************************
if reuseData == False:
	collectedData = scrapeTopic(topic,tweetLim,dates)
	if collectedData.empty:
		print('No network for:',topic)
		exit(0)
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
f = plt.figure(figsize=[10, 8])
plt.axis('off')
plt.title(topic.title() + ' ' + centralityType,fontweight='bold')
mySociogram.calcFeatures(topN,centralitySelected)
mySociogram.drawNetwork()
plt.tight_layout()
f.savefig(topic.title() + ' ' + centralityType + ' sociogram.jpg')

mySociogram.saveSummary(topic.title() + ' ' + centralityType + ' summary.csv') # (topic +' summary.csv')

input("Press Enter to close all plots...")
