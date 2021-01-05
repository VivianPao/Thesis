
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

# DEPICT WHOLE NETWORK

# Setting colors based on followers
# commDict = dict()

# for X in range(42):
# 	csv = pd.read_csv('comm'+str(X)+'.csv',index_col=0)	# Be careful with indexing. Name the column 'username'
# 	memberList = list(csv['degree'])
# 	commDict[X] = memberList
# colorDict = assignCommunityColors(commDict)

# Relevant communities only
allMembers = []
over50 = range(42)#[2,6,9,15]#[0,1,2,3,4,6,7,8,9,12,13,14,15]
for i in range(len(over50)):
	X = over50[i]
	csv = pd.read_csv('comm'+str(X)+'.csv',index_col=0)	# Be careful with indexing. Name the column 'username'
	memberList = list(csv['degree'])
	allMembers = allMembers + memberList
# 	commDict[i] = memberList
# colorDict = assignCommunityColors(commDict)

# For individual communities
# colorDict = dict(zip(memberList,['mediumorchid']*len(memberList)))


# Calculate overall centrality
# N = 10

subject = 'Position of flyWSA -'



# POSTS NETWORK

# df = keepOnlyUsers(postsDf,allMembers,strictFilterCol='reply_to')

# cDf = calcOverallCentrality(df,'reply_to')
# degreeSorted = cDf.sort_values(by='degree',ascending=False)
# eigenvectorSorted = cDf.sort_values(by='eigenvector',ascending=False)
# betweennessSorted = cDf.sort_values(by='betweenness',ascending=False)
# closenessSorted = cDf.sort_values(by='closeness',ascending=False)
# overallSorted = cDf.sort_values(by='closeness',ascending=False)

# commMembers = pd.DataFrame()
# commMembers['degree'] = list(degreeSorted['username'])
# commMembers['betweenness'] = list(betweennessSorted['username'])
# commMembers['eigenvector'] = list(eigenvectorSorted['username'])
# commMembers['closeness'] = list(closenessSorted['username'])
# commMembers['overall'] = list(overallSorted['username'])
# commMembers.to_csv(subject+' reply centrality'+'.csv')
# overallCenDict = dict(zip(list(cDf['username']),list(cDf['betweenness'])))
overallCenDict = None
overallCenDict = {'flyWSA':3}
# labelList = list(commMembers['betweenness'])
# labelList = labelList[:N]
colorDict = {'flyWSA':'r'}
labelList = 'flyWSA'

# df,keepList,strictFilterCol
# top10df = keepOnlyUsers(df,labelList,strictFilterCol='reply_to')

# drawGraph(top10df,'reply_to',title=subject+'top 10 replies w Comm Color',labelList=labelList,colorDict=colorDict,sizesDict=overallCenDict,sizeScale=100,minSize=5,removeIsolates=True,edgeAlpha=0.05,block=False,saveAndClose=True)


# drawGraph(postsDf,'reply_to',title=subject+'Full Replies',labelList=labelList,colorDict=colorDict,sizesDict=overallCenDict,sizeScale=100,minSize=5,removeIsolates=True,edgeAlpha=0.05,block=False,saveAndClose=True)







# # FOLLOWS NETWORK
df = keepOnlyUsers(followsDf,allMembers,strictFilterCol='followings')

cDf = calcOverallCentrality(followsDf,'followings')
# degreeSorted = cDf.sort_values(by='degree',ascending=False)
# eigenvectorSorted = cDf.sort_values(by='eigenvector',ascending=False)
# betweennessSorted = cDf.sort_values(by='betweenness',ascending=False)
# closenessSorted = cDf.sort_values(by='closeness',ascending=False)
overallSorted = cDf.sort_values(by='overall',ascending=False)
overallSorted.to_csv(subject+' follower centrality'+'.csv')
# commMembers = pd.DataFrame()
# # commMembers['degree'] = list(degreeSorted['username'])
# commMembers['betweenness'] = list(betweennessSorted['username'])
# # commMembers['eigenvector'] = list(eigenvectorSorted['username'])
# # commMembers['closeness'] = list(closenessSorted['username'])
# commMembers['overall'] = list(overallSorted['username'])
# # commMembers.to_csv(subject+' follower centrality'+'.csv')
# overallCenDict = dict(zip(list(cDf['username']),list(cDf['betweenness'])))
# # overallCenDict = None
# overallCenDict = None
# labelList = list(commMembers['betweenness'])
# labelList = labelList[:N]


# # top10df = keepOnlyUsers(df,labelList,strictFilterCol='followings')

# # drawGraph(top10df,'followings',title=subject+'top 10 followings w Comm Color',labelList=labelList,colorDict=colorDict,sizesDict=overallCenDict,sizeScale=100,minSize=5,removeIsolates=True,edgeAlpha=0.05,block=False,saveAndClose=True)


# drawGraph(df,'followings',title=subject+'Full Followings w Comm Color',labelList=labelList,colorDict=colorDict,sizesDict=overallCenDict,sizeScale=100,minSize=5,removeIsolates=True,edgeAlpha=0.05,block=False,saveAndClose=True)
