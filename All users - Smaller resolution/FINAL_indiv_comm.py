
import pandas as pd
from FINAL_fns import *

######################## USER INPUTS #######################
filename = "allPosts.csv"
# filename = "allFollowings.json"
topN = 100
title = 'Something'

def drawCommFromFile(filename,topN,title):
	
	######################## LOAD THE DATA #######################
	if ".csv" in filename:
		df = pd.read_csv(filename)
	else:
		df = pd.read_json(filename)

	dataType = checkRepliesOrFollows(df)
	if dataType == REPLIES:
		typeString = 'reply_to'
		subtitle = 'Communities Based On Replies: '
		df['reply_to'] = df['reply_to'].apply(turn2LiteralKeysReply)

	elif dataType == FOLLOWS:
		typeString = 'followings'
		subtitle = 'Communities Based On Follows: '
		df['followings'] = df['followings'].apply(turn2LiteralKeys)


	######################## PROCESS AND VISUALISE #######################
	commDict = extractCommunities(df,typeString,reciprocal=True,individualsAsCommunities=False)

	for i in range(len(commDict)):
		commList = commDict[i]
		commDf = keepOnlyUsers(df,commList,strictFilterCol=typeString)
		cDf = calcOverallCentrality(commDf,typeString)
		overallCenDict = dict(zip(list(cDf['username']),list(cDf['overall'])))
		overallSorted = cDf.sort_values(by='overall',ascending=False)
		labelList = list(overallSorted['username'])
		labelList = labelList[:topN]

		drawGraph(commDf,typeString,title=subtitle+'('+str(i)+') '+title,sizesDict=overallCenDict,labelList=labelList,sizeScale=100,minSize=5,removeIsolates=False,edgeAlpha=0.05,block=False,saveAndClose=True)
