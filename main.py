
from Sociogram import *
from getDates import getMonthlyDates
from readWriteData import *
from twitterScraping import *

# ************ USER INPUTS *************************************

newData = False
topN = 10
dates = ['2006-01-01','2020-09-12']	# YYYY-MM-DD
topic = 'badgerys creek airport'
centralityType = 'degree' # Choose from 'in degree','out degree','degree','eigenvector','closeness','betweenness'
tweetLim = None

# ************ MAIN ******************************************** 

dateWindowList = [dates]
dateWindowList = getMonthlyDates(dates[0],dates[1]) # Show network using these monthly date pairs

for dateWindow in dateWindowList:	# Loop through all windows in list
	title = topic.title() + ' ' + dateWindow[0] + ' to ' + dateWindow[1]
	if newData:
		collectedData = scrapeTopic(topic,tweetLim,dateWindow)
	else:
		collectedData = readDataCSV('data ' + title + '.csv')

	if collectedData.empty:
		print('No network for:',topic)
		continue
	elif newData and collectedData.empty == False:
		collectedData.to_csv('data ' + title + '.csv',index=False)

	mySociogram = Sociogram(collectedData,title,topN,centralityType)
	mySociogram.saveSummary('summary ' + title + ' .csv')
	plt.savefig('sociogram ' + title + 'sociogram.jpg')
	plt.show(block=False)

input("Press Enter to close all plots...")

# Added functionality to visualise networks that have nodes and no edges. Dealt with cases of data files not existing.