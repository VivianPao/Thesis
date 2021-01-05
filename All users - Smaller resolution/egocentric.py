
# Unidirectional egocentric networks: replies and follows

import pandas as pd
from sociogramFunctions import *

def __mergeDictCol__(dfColumn):
	dictList = list(dfColumn)
	dictList = [d for d in dictList if d != {}]
	edgesDict = dict(ChainMap(*dictList))	# Merge all dictionaries
	return edgesDict

def getEgocentricDf(df,column,username):
	newDf = __filterEgocentric__(df,column,username)
	isolates = listIsolates(newDf,column,exceptedList=[username])
	newDf = newDf[~newDf.username.isin(isolates)]
	return newDf

# Result: get a df with only the users. Go through edges dict to keep only specified users too
def __filterEgocentric__(df,column,user):
	newDf = df.copy()
	newDf[column] = newDf[column].apply(__filterDictEgo__,user=user)
	return newDf

# Remove user from dictionary first. Get all users df regarding user and then get the user.
def __filterDictEgo__(currLinkDict,user):

	# If the dictionary is empty, keep it empty
	if hasattr(currLinkDict,'items') == 0:
		return currLinkDict

	keyList = list(currLinkDict.keys())
	newLinkDict = {key:currLinkDict[key] for key in keyList if user == key[0] or user == key[1]}
	return newLinkDict

def turn2LiteralKeysReply(dictionary):
	return eval(dictionary)

postsDf = pd.read_csv('allPosts.csv')
postsDf['reply_to'] = postsDf['reply_to'].apply(turn2LiteralKeysReply)
followsDf = pd.read_json('allFollowings.json')
followsDf['followings'] = followsDf['followings'].apply(turn2LiteralKeys)

user = 'Greens'








egoPost = getEgocentricDf(postsDf,'reply_to',user)
egoFollows = getEgocentricDf(followsDf,'followings',user)

# To and from versions
egoPost_to = egoPost.loc[egoPost['username'] != user]
egoPost_from = egoPost.loc[egoPost['username'] == user]
egoFollows_to = egoFollows.loc[egoFollows['username'] != user]
egoFollows_from = egoFollows.loc[egoFollows['username'] == user]

# print(len(egoPost_to))
# print(len(egoPost_from))
# print(len(egoFollows_to))
# print(len(egoFollows_from))



# Setting colors
commDict = dict()

over50 = [0,1,2,3,4,6,7,8,9,12,13,14,15]

for i in range(len(over50)):# for X in range(42):
	X = over50[i]
	csv = pd.read_csv('comm'+str(X)+'.csv',index_col=0)	# Be careful with indexing. Name the column 'username'
	memberList = list(csv['degree'])
	commDict[i] = memberList
colorDict = assignCommunityColors(commDict)


####################################

drawGraph(egoPost_to,'reply_to',title=user+'-Egocentric Who replies to '+user+' (with labels)',block=False,sizesDict={user:3},colorDict=colorDict,labelList=list(egoPost_to['username'])+[user],edgeAlpha=0.1,saveAndClose=True)
drawGraph(egoPost_to,'reply_to',title='Egocentric Who replies to '+user,block=False,sizesDict={user:3},colorDict=colorDict,edgeAlpha=0.1,saveAndClose=True)

####################################

drawGraph(egoFollows_to,'followings',title=user+'-Egocentric: Who follows '+user+' (with labels)',block=False,sizesDict={user:3},colorDict=colorDict,labelList=list(egoFollows_to['username'])+[user],edgeAlpha=0.1,saveAndClose=True)
drawGraph(egoFollows_to,'followings',title='Egocentric: Who follows '+user,block=False,sizesDict={user:3},colorDict=colorDict,edgeAlpha=0.1,saveAndClose=True)

####################################

edgeDict = __mergeDictCol__(egoPost_from['reply_to'])
edgeList = list(edgeDict.keys())
labelList = [edge[1] for edge in edgeList]	# Retrieve the 'to'
drawGraph(egoPost_from,'reply_to',title=user+'-Egocentric Who '+user+' replies to'+' (with labels)',block=False,sizesDict={user:3},colorDict=colorDict,labelList=labelList+[user],edgeAlpha=0.1,saveAndClose=True)
drawGraph(egoPost_from,'reply_to',title=user+'-Egocentric Who '+user+' replies to',block=False,sizesDict={user:3},colorDict=colorDict,edgeAlpha=0.1,saveAndClose=True)

####################################

edgeDict = __mergeDictCol__(egoFollows_from['followings'])
edgeList = list(edgeDict.keys())
labelList = [edge[1] for edge in edgeList]	# Retrieve the 'to'
drawGraph(egoFollows_from,'followings',title=user+'-Egocentric Who '+user+' follows'+' (with labels)',block=False,sizesDict={user:3},colorDict=colorDict,labelList=labelList+[user],edgeAlpha=0.1,saveAndClose=True)
drawGraph(egoFollows_from,'followings',title=user+'-Egocentric Who '+user+' follows',block=False,sizesDict={user:3},colorDict=colorDict,edgeAlpha=0.1,saveAndClose=True)
