
import pandas as pd
import ast

def readDataCSV(nameFile):	# Dicts by default in string format. Rewrite the column with real dicts.
	collectedData = pd.read_csv(nameFile)
	weightedLinks = collectedData['reply_to'].tolist()	# List of dicts
	columnIndex = collectedData.columns.get_loc('reply_to')
	for i in range(len(weightedLinks)):		
		collectedData.iloc[i,columnIndex] = [ast.literal_eval(weightedLinks[i])]
	return collectedData

# def getNewData(topic,tweetLim,dates,filename):
# 	collectedData = scrapeTopic(topic,tweetLim,dates)
# 	collectedData.to_csv(filename,index=False)
# 	return collectedData