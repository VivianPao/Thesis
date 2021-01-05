
import pandas as pd
from FINAL_fns import *

######################## USER INPUTS #######################
# filename = "allPosts.csv"
filename = "allFollowings.json"
topN = 100
title = 'Whole network'

def generateWholeNetworkFromFile(filename,topN,title):
	######################## LOAD THE DATA #######################
	if ".csv" in filename:
		df = pd.read_csv(filename)
	else:
		df = pd.read_json(filename)

	dataType = checkRepliesOrFollows(df)
	if dataType == REPLIES:
		typeString = 'reply_to'
		subtitle = 'Replies: '
		df['reply_to'] = df['reply_to'].apply(turn2LiteralKeysReply)

	elif dataType == FOLLOWS:
		typeString = 'followings'
		subtitle = 'Follows: '
		df['followings'] = df['followings'].apply(turn2LiteralKeys)


	######################## PROCESS AND VISUALISE #######################
	cDf = calcOverallCentrality(df,typeString)
	overallCenDict = dict(zip(list(cDf['username']),list(cDf['overall'])))
	overallSorted = cDf.sort_values(by='overall',ascending=False)
	labelList = list(overallSorted['username'])
	labelList = labelList[:topN]

	drawGraph(df,typeString,title=subtitle+title,sizesDict=overallCenDict,labelList=labelList,sizeScale=100,minSize=5,removeIsolates=False,edgeAlpha=0.05,block=False,saveAndClose=True)
