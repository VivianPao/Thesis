
# Unidirectional egocentric networks: replies and follows

import pandas as pd
from sociogramFunctions import *

def __mergeDictCol__(dfColumn):
	dictList = list(dfColumn)
	dictList = [d for d in dictList if d != {}]
	edgesDict = dict(ChainMap(*dictList))	# Merge all dictionaries
	return edgesDict

def turn2LiteralKeysReply(dictionary):
	return eval(dictionary)

postsDf = pd.read_csv('allPosts.csv')
postsDf['reply_to'] = postsDf['reply_to'].apply(turn2LiteralKeysReply)
followsDf = pd.read_json('allFollowings.json')
followsDf['followings'] = followsDf['followings'].apply(turn2LiteralKeys)

# Setting colors based on followers
commDict = dict()

# Relevant communities only
allMembers = []
over50 = [0,1,2,3,4,6,7,8,9,12,13,14,15]
for i in range(len(over50)):
	X = over50[i]
	csv = pd.read_csv('comm'+str(X)+'.csv',index_col=0)	# Be careful with indexing. Name the column 'username'
	memberList = list(csv['degree'])
	allMembers = allMembers + memberList
	commDict[X] = memberList


allMembers = []
over50 = [0,1,2,3,4,6,7,8,9,12,13,14,15]
for i in range(len(over50)):
	X = over50[i]
	memberList = commDict[X]

	# FOLLOWS NETWORK
	df = keepOnlyUsers(followsDf,memberList,strictFilterCol='followings')
	cDf = calcOverallCentrality(df,'followings')
	overallSorted = cDf.sort_values(by='overall',ascending=False)
	overallSorted.to_csv('oCentrality_comm'+str(X)+'.csv')
