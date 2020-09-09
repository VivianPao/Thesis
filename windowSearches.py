
import pandas as pd
import ast
from twitterScraping import *
from Sociogram import *

# main.py is able to reload old data again. Introduce this functionality and we'll be good.

# ***************************************************************
# CONSTANTS
# ***************************************************************
[IN_DEG_CEN,OUT_DEG_CEN,DEG_CEN,EIG_CEN,CLOSE_CEN,BTWN_CEN] = range(0,6)
CENTRALITY = {'in degree':IN_DEG_CEN,'out degree':OUT_DEG_CEN,'degree':DEG_CEN,'eigenvector':EIG_CEN,'closeness':CLOSE_CEN,'betweenness':BTWN_CEN}

# ***************************************************************
# USER INPUTS
# ***************************************************************
reuseData = False
tweetLim = None#10#10000
topN = 10
userDateList = ['2014-04-15 0:0:0','2015-01-20 0:0:0','2015-10-19 0:0:0','2017-05-09 0:0:0','2018-09-24 0:0:0']
topic = 'badgerys creek airport' # Or list of topics ['chicken','beef']
centralityType = 'degree' # Or List ['degree','betweenness']

# Check if it works for none, for 1, with prepend/append, collect ALL data! (do on desktop to keep it running in the background. Install packages etc. get git working on Windows)
dateList = ['2006-01-01 0:0:0']		# Twitter's creation date
for date in userDateList:
	dateList.append(date)
dateList.append('2020-09-09 0:0:0')		# Today's date

# ***************************************************************
# SCRAPING AND VISUALISATIONS
# ***************************************************************

# Find the networks within each time window
for i in range(len(dateList)-1):
	dates = [dateList[i],dateList[i+1]]
	dateString = str(dates[0]) + '_' +  str(dates[1])
	print(dateString)

	# ***************************************************************
	# TWITTER SCRAPING
	# ***************************************************************
	
	if reuseData == False:
		collectedData = scrapeTopic(topic,tweetLim,dates)
		if collectedData.empty:
			print('No network for:',topic)
			# Create file for the time periods that have no activity as well so the code doesn't break when you're reading in old data. Make sure to have the headings too.
			continue
		collectedData.to_csv('data_' + dateString + '.csv',index=False)
	else:	# Dicts by default in string format. Rewrite the column with real dicts.
		collectedData = pd.read_csv('data_' + dateString + '.csv')
		weightedLinks = collectedData['reply_to'].tolist()	# List of dicts
		columnIndex = collectedData.columns.get_loc('reply_to')
		for i in range(len(weightedLinks)):		
			collectedData.iloc[i,columnIndex] = [ast.literal_eval(weightedLinks[i])]

	# ***************************************************************
	# VISUALISATION
	# ***************************************************************

	mySociogram = Sociogram(collectedData)

	# Create figure and save as image
	f = plt.figure(figsize=[10, 8])
	plt.axis('off')
	plt.title(topic.title() + ' ' + dateString,fontweight='bold')
	mySociogram.calcFeatures(topN,CENTRALITY[centralityType])
	mySociogram.drawNetwork()
	plt.tight_layout()
	f.savefig(topic.title() + ' ' + dateString + ' sociogram.jpg')

	mySociogram.saveSummary(topic.title() + ' ' + dateString + ' summary.csv') # (topic +' summary.csv')

input("Press Enter to close all plots...")

