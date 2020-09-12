from Sociogram import *
from getDates import getMonthlyDates, getYearlyDates
from readWriteData import *
from twitterScraping import *

# ************ USER INPUTS *************************************

topN = 10
dates = ['2020-01-01','2020-09-12']	# YYYY-MM-DD
topic = 'badgerys creek airport'
centralityType = 'degree'	# Choose from 'in degree','out degree','degree','eigenvector','closeness','betweenness'

tweetLim = None
divideType = 'monthly' #'yearly'		# Choose from None, 'monthly' or 'yearly'
newData = False
showFigures = True
saveFigures = True

# ************ MAIN ******************************************** 

# GET DATA. If getting new data and data exists, save to csv. If not, read from csv. If empty df, exit.
title = topic.title() + ' ' + dates[0] + ' to ' + dates[1]
if newData:
	collectedData = scrapeTopic(topic,tweetLim,dates)
	if collectedData.empty == False:
		collectedData.to_csv('data ' + title + '.csv',index=False)
else:
	collectedData = readDataCSV('data ' + title + '.csv')
if collectedData.empty:
	print('No network for:',title)
	exit(0)

# Setting automatic windows. Monthly ignores days, Yearly ignores monthly/ days.
if divideType == None: dateWindowList = [dates]
if divideType == 'monthly': dateWindowList = getMonthlyDates(dates[0],dates[1]) # Use monthly date pairs
if divideType == 'yearly': dateWindowList = getYearlyDates(dates[0],dates[1]) # Use yearly date pairs

# For each window, visualise the sociogram
for dateWindow in dateWindowList:
	windowData = collectedData[(collectedData['date'] >= dateWindow[0]) & (collectedData['date'] <= dateWindow[1])]
	if windowData.empty:
		print('No network for window:',title)
		continue

	title = topic.title() + ' ' + dateWindow[0] + ' to ' + dateWindow[1]
	mySociogram = Sociogram(windowData,title,topN,centralityType)

	if saveFigures:
		mySociogram.saveSummary(title + ' summary.csv')
		plt.savefig(title + ' sociogram.jpg')
	if showFigures:
		plt.show(block=False)
if showFigures:
	input("Press Enter to close all plots...")
