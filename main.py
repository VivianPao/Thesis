
from Sociogram import *
from getDates import getMonthlyDates
from readWriteData import *
from twitterScraping import *

# ***************************************************************
# USER INPUTS
# ***************************************************************

newData = False
topN = 10
dates = ['2020-09-05','2020-09-12']	# YYYY-MM-DD
topic = 'badgerys creek airport'
centralityType = 'degree' # Choose from 'in degree','out degree','degree','eigenvector','closeness','betweenness'
tweetLim = None

# ***************************************************************
# MAIN
# ***************************************************************
dateWindowList = [dates]
# dateWindowList = getMonthlyDates(dates[0],dates[1]) # Show network using these monthly date pairs

for dateWindow in dateWindowList:	# Loop through all windows in list for month break down...	
	title = topic.title() + ' ' + dateWindow[0] + ' to ' + dateWindow[1]
	if newData:
		collectedData = scrapeTopic(topic,tweetLim,dates)
		collectedData.to_csv(filename,index=False)
		if collectedData.empty:
			print('No network for:',topic)
			continue
	else:
		collectedData = readDataCSV(title + '.csv')
	
	mySociogram = Sociogram(collectedData,title,topN,centralityType)
	mySociogram.saveSummary(title + ' summary.csv')
	plt.savefig(title + ' sociogram.jpg')
	plt.show(block=False)

input("Press Enter to close all plots...")

# Pending Improvements:
# - Sentiment analysis
# - Error catching edge cases for empty searches/ when reading files that don't exist.
# - More detailed csv summary. Include in-deg, out-deg, network density & sentiment count for whole network
# - Creating functions to visualise network changes better, using CV to stack images, label and save?