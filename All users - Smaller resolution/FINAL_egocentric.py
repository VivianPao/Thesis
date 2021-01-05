
from FINAL_fns import *
import pandas as pd

######################## USER INPUTS #######################
# filename = "allPosts.csv"
# # filename = "allFollowings.json"
# user = "Greens"

def generateEgocentricFromFile(filename,user):

	######################## LOAD THE DATA #######################
	if ".csv" in filename:
		df = pd.read_csv(filename)
	else:
		df = pd.read_json(filename)


	######################## PROCESS DATA AND VISUALISE #######################
	dataType = checkRepliesOrFollows(df)
	if dataType == REPLIES:
		df['reply_to'] = df['reply_to'].apply(turn2LiteralKeysReply)
		egoPost = getEgocentricDf(df,'reply_to',user)

		egoPost_to = egoPost.loc[egoPost['username'] != user]
		egoPost_from = egoPost.loc[egoPost['username'] == user]

		# INCOMING CONNECTIONS
		drawGraph(egoPost_to,'reply_to',title='Egocentric: Who replies to '+user,block=False,sizesDict={user:3},labelList=list(egoPost_to['username'])+[user],edgeAlpha=0.1,saveAndClose=True)

		# OUTGOING CONNECTIONS
		edgeDict = mergeDictCol(egoPost_from['reply_to'])
		edgeList = list(edgeDict.keys())
		labelList = [edge[1] for edge in edgeList]	# Retrieve the 'to'
		drawGraph(egoPost_from,'reply_to',title='Egocentric: Who '+user+' replies to',block=False,sizesDict={user:3},labelList=labelList+[user],edgeAlpha=0.1,saveAndClose=True)

	elif dataType == FOLLOWS:
		df['followings'] = df['followings'].apply(turn2LiteralKeys)
		egoFollows = getEgocentricDf(df,'followings',user)

		egoFollows_to = egoFollows.loc[egoFollows['username'] != user]
		egoFollows_from = egoFollows.loc[egoFollows['username'] == user]

		# INCOMING CONNECTIONS
		drawGraph(egoFollows_to,'followings',title='Egocentric: Who follows '+user,block=False,sizesDict={user:3},labelList=list(egoFollows_to['username'])+[user],edgeAlpha=0.1,saveAndClose=True)

		# OUTGOING CONNECTIONS
		edgeDict = mergeDictCol(egoFollows_from['followings'])
		edgeList = list(edgeDict.keys())
		labelList = [edge[1] for edge in edgeList]	# Retrieve the 'to'
		drawGraph(egoFollows_from,'followings',title='Egocentric: Who '+user+' follows',block=False,sizesDict={user:3},labelList=labelList+[user],edgeAlpha=0.1,saveAndClose=True)

filename = "allPosts.csv"
user = "Greens"

generateEgocentricFromFile(filename,user)