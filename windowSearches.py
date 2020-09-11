
import pandas as pd
from Sociogram import *
from getDates import getMonthlyDates
from readWriteData import *

# ***************************************************************
# USER INPUTS
# ***************************************************************

newData = True
tweetLim = None
topN = 10
dates = ['2020-05-01','2020-09-01']	# YYYY-MM-DD
topic = 'badgerys creek airport'
centralityType = 'degree' # Choose from 'in degree','out degree','degree','eigenvector','closeness','betweenness'

# ***************************************************************
# CREATING SEARCH WINDOWS
# ***************************************************************

dateWindow = dates
# dateWindowList = getMonthlyDates(dates[0],dates[len(dates)-1]) # Show network using these monthly date pairs
# dateWindow = dateWindowList[0]	# Loop through all windows in list for month break down

# ***************************************************************
# MAIN
# ***************************************************************
title = topic.title() + ' ' + dates[0] + ' to ' + dates[1]
if newData:
	collectedData = getNewData(topic,tweetLim,dateWindow,title + '.csv');
else:
	collectedData = readDataCSV(title + '.csv')
mySociogram = Sociogram(collectedData,title,topN,centralityType)
mySociogram.saveSummary(title + ' summary.csv')

# Show sociogram
plt.savefig(title + ' sociogram.jpg')
plt.show(block=False)
input("Press Enter to close all plots...")