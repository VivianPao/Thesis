
# FINAL_fns

import twint
from ast import literal_eval
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
from collections import ChainMap 
import matplotlib.cm as cm
import community as community_louvain

REPLIES = 0
FOLLOWS = 1
INVALID = -1

# TWITTER SCRAPING FUNCTIONS

# If the user has been seen before, increment their count. If not, add them into the dictionary and set count to 1.
def addToDict(dictName,keyValue):
	if keyValue not in dictName:
		dictName[keyValue] = 1
	else:
		dictName[keyValue] += 1

# Return dataframe with sentiment analysis and edge + weight dictionary
def organiseData(df):

	if df.empty:
		return df

	df = df[['date','username','tweet','reply_to']]	# concat string tweets and list of dicts
	df = df.groupby('username',as_index=False).aggregate(sum)	# Group by username (merge duplicates)

	# print(df)

	# For each user/ row, rewrite the dictionary. key: mentioned users, val: weight
	# Use the apply() pandas function to create a new entry for the dictionary!
	for row in range(len(df)):
		username = df.iloc[row][0]
		listOfDicts = df.iloc[row]['reply_to']

		linkTo = {}	# Create dict, keys as tuples of user -> mentioned user: weight
		for aDict in listOfDicts:
			mentionedUser = aDict['screen_name']
			if mentionedUser != username: # As long as the user isn't replying to themselves, add them to the dictionary
				addToDict(linkTo,(username,mentionedUser))
		df.loc[df.username == username,'reply_to'] = [linkTo]

	# df['sentiment'] = df['tweet'].apply(calcTextSentiment)	# Add sentiment column

	return df

# Need to process/ reoganise the followings
def organiseFollows(df):
	return 0

# Based on the posts of a topic, find all the users that have mentioned a particular person on a topic (or no topic)
def scrapeTopic(topic,tweetLimit=None,dates=None):
# Dates in form ['YYYY-MM-DD','YYYY-MM-DD']
	c = twint.Config()

	if tweetLimit != None:
		c.Limit = tweetLimit
	
	c.Search = topic
	# c.Store_csv = True
	# The following features/ customisations do not work with the latest Twint version
	c.Pandas = True
	# c.Format = "{date}: {username} -> {mentions}" 
	if dates != None:
		[sinceDate,untilDate] = dates
		c.Since = sinceDate
		c.Until = untilDate

	twint.run.Search(c)

	df = organiseData(twint.storage.panda.Tweets_df)

	return df	# Dataframe of series!


def findFollowing(username,limitNum=10000):
	c = twint.Config()
	# c.Limit = limitNum
	c.Pandas = True
	c.Username = username
	twint.run.Following(c)

	collectedData = twint.storage.panda.Follow_df	# Dataframe of dataframes!
	targetData = collectedData.loc[:,('following')][username]	# Gives an array
	sourceData = [username] * len(targetData)
	finalData = pd.DataFrame({'A': sourceData,'B': targetData})
	# print(finalData)
	return finalData

def scrapeFollowings(userList):
	followerDf = pd.DataFrame()
	for user in userList:
		print('Searching: ',user)
		for attempt in range(10):
			try:
				data = findFollowing(user,None)
			except:
				print('Error for',user)
				continue
			followerDf = pd.concat([followerDf,data])
			followerDf.to_csv('followerData'+userList[len(userList)-1]+'.csv')
			break

	return followerDf

# DRAWING FILE

def drawCommFromFile(filename,topN):
	
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

		drawGraph(commDf,typeString,title=filename+'- '+subtitle+'('+str(i)+') ',sizesDict=overallCenDict,labelList=labelList,sizeScale=100,minSize=5,removeIsolates=False,edgeAlpha=0.05,block=False,saveAndClose=True)


def drawWholeNetworkFromFile(filename,topN):
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

	drawGraph(df,typeString,title=filename+'- '+subtitle,sizesDict=overallCenDict,labelList=labelList,sizeScale=100,minSize=5,removeIsolates=False,edgeAlpha=0.05,block=False,saveAndClose=True)


def drawEgoFromFile(filename,user):

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




######################## FUNCTIONS #######################
def checkRepliesOrFollows(fileDf):
	headingsList = list(fileDf.columns)
	if 'reply_to' in headingsList:
		# print('Replies')
		return REPLIES
	elif 'followings' in headingsList:
		# print('Followings')
		return FOLLOWS
	else:
		# print('Not a valid csv')
		return INVALID

def sentiment2Color(score):
	if score < 0:
		return 'r'
	elif score > 0:
		return 'g'
	else:
		return 'y'

def analyseCalls2Action(text):
	wordBank = ["petition","protest","letter","strike"]
	score = 0
	for word in wordBank:
		score += text.count(word)
	return score

def calls2Action2Color(text):
	score = analyseCalls2Action(text)
	if score > 0:
		return 'r'
	else:
		return 'gray'

def calcOverallCentrality(df,columnName):
	edgeDict = mergeDictCol(df[columnName])
	G = nx.Graph()
	G.add_edges_from(edgeDict)

	centralityDf = pd.DataFrame()
	centralityDf['username'] = list(G.nodes())
	centralityDf['degree'] = __calcCentrality__(G,centralityType='degree')
	centralityDf['eigenvector'] = __calcCentrality__(G,centralityType='eigenvector')
	centralityDf['closeness'] = __calcCentrality__(G,centralityType='closeness')
	centralityDf['betweenness'] = __calcCentrality__(G,centralityType='betweenness')

	centralityDf['degree'] = (centralityDf['degree'] - min(list(centralityDf['degree'])))/(max(list(centralityDf['degree']))-min(list(centralityDf['degree'])))
	centralityDf['eigenvector'] = (centralityDf['eigenvector'] - min(list(centralityDf['eigenvector'])))/(max(list(centralityDf['eigenvector']))-min(list(centralityDf['eigenvector'])))
	centralityDf['closeness'] = (centralityDf['closeness'] - min(list(centralityDf['closeness'])))/(max(list(centralityDf['closeness']))-min(list(centralityDf['closeness'])))
	centralityDf['betweenness'] = (centralityDf['betweenness'] - min(list(centralityDf['betweenness'])))/(max(list(centralityDf['betweenness']))-min(list(centralityDf['betweenness'])))

	centralityDf['overall'] = centralityDf['degree'] + centralityDf['eigenvector'] + centralityDf['closeness'] + centralityDf['betweenness']

	return centralityDf

def assignColor(userList,color):
	colorDict = {user: color for user in userList}
	return colorDict

def assignCommunityColors(communitiesDict,maxCommNum=None):
	if maxCommNum == None:
		numGroups = len(communitiesDict)
	else:
		numGroups = maxCommNum

	# Prep colors from color map chosen
	cMapping = cm.get_cmap('hsv',numGroups+1)	# To avoid color map looping.
	colorList = cMapping(range(numGroups+1))

	colorDict = dict()

	for groupNum in range(numGroups):
		color = colorList[groupNum]
		userList = communitiesDict[groupNum]
		subColorDict = assignColor(userList,color)
		# subColorDict = {user: color for user in userList}
		colorDict.update(subColorDict)

	return colorDict

def turn2LiteralKeys(dictionary):
	keys = dictionary.keys()
	vals = dictionary.values()
	realKeys = [literal_eval(k) for k in keys]
	return dict(zip(realKeys,vals))
	
def restructureFollowingsDf(followerData0):
	followerData0 = followerData0[['A','B']]		# Remove indexing column
	followerData0 = followerData0.groupby('A',as_index=False).agg(list)

	# Write to new dataframe with meaningful column names
	restructuredDf = pd.DataFrame()
	restructuredDf['username'] = followerData0['A']
	restructuredDf['followings'] = followerData0.apply(lambda x: __list2EdgeDict__(x['A'],x['B']),axis=1)
	return restructuredDf

# Consider individuals as communities. To remove isolates, use the function you wrote.
def extractCommunities(df,columnName,reciprocal=False,individualsAsCommunities=True):

	nodes = list(df['username'])
	edges = mergeDictCol(df[columnName])
	# print(edges)

	G = nx.DiGraph()
	G.add_nodes_from(nodes)	# Ensures the top 100 nodes are first in list
	G.add_edges_from(edges)
	G = G.to_undirected(reciprocal=reciprocal)
	if individualsAsCommunities == False:
		G.remove_nodes_from(list(nx.isolates(G)))

	partition = community_louvain.best_partition(G)

	# Restructure partitions into lists of users for each group.
	# {0: [a,b,c,d],1: [e,f,g]}

	userList = list(partition.keys())
	groupAllocationList = list(partition.values())
	
	# If no groups detected, return empty dictionary
	if len(groupAllocationList) == 0:
		print("\nNo communities found :(\n")
		return dict()

	numGroups = max(groupAllocationList)+1

	communitiesDict = dict()
	for groupNum in range(numGroups):
		# Go through every user, if their group number matches, add username to list
		groupList = [userList[i] for i in range(len(userList)) if groupAllocationList[i] == groupNum]
		communitiesDict[groupNum] = groupList

	return communitiesDict

########## PRIVATE
def __list2EdgeDict__(colA,colB):
	userA = colA
	userBList = colB
	
	followDict = {(userA,userB): 1 for userB in userBList}

	return followDict


# Find centrality of each user and group into ranges. Have 3 different sizes.
def centralityRange(df,columnName,centralityType='degree'):
	edgesDict = mergeDictCol(df[columnName])
	
	G = nx.DiGraph()
	G.add_edges_from(edgesDict)

	users = list(G.nodes())
	centralityList = __calcCentrality__(G,centralityType=centralityType)
	cDf = pd.DataFrame()
	cDf['centralityList'] = centralityList
	# print(cDf)

	div = 3
	maxC = max(centralityList)
	minC = min(centralityList)
	cDf = cDf['centralityList'].apply(roundIntoRange,minV=minC,maxV=maxC,div=div)

	centralitySizes = dict(zip(users,list(cDf)))
	return centralitySizes

def roundIntoRange(value,minV,maxV,div):
	rangeList = np.linspace(minV,maxV,div)
	rangeList[len(rangeList)-1] += 0.1	# Increase the last element so that we can easily put into a range

	for i in range(len(rangeList)-1):
		rangeMin = rangeList[i]
		rangeMax = rangeList[i+1]
		print('Range: '+str(rangeMin)+','+str(rangeMax))

		if value >= rangeMin and value < rangeMax: return i+1

	return 0


# Accept a dictionary of usernames and their relative size
def __calcSizes__(G,dictUserSize,scaleUp,minSize):
	networkUserList = list(G.nodes())
	dictUserList = list(dictUserSize.keys())

	# Set user to white if they're not in the dictionary. Otherwise, set their color
	sizeArray = [dictUserSize[user] if user in dictUserList else 1 for user in networkUserList]

	# Scale for number of nodes
	sizeArray = [val*scaleUp if val != 1 else minSize for val in sizeArray]

	return sizeArray

# Accept a dictionary of usernames and their color
def __calcColors__(G,dictUserColor):
	networkUserList = list(G.nodes())
	dictUserList = list(dictUserColor.keys())

	# Set user to white if they're not in the dictionary. Otherwise, set their color
	colorArray = [dictUserColor[user] if user in dictUserList else 'gray' for user in networkUserList]
	return colorArray

# Accept a dictionary of tuple username connections, connection strength
def __calcEdgeWidth__(G,dictEdge,widthScale):
	networkUserList = list(G.edges())
	dictUserList = list(dictEdge.keys())

	widthArray = [dictEdge[user] if user in dictUserList else 1 for user in networkUserList]
	widthArray = [val*widthScale for val in widthArray]
	return widthArray

def __calcCentrality__(G,centralityType='degree'):
	if centralityType == 'indegree':
		return list(nx.in_degree_centrality(G).values())
	elif centralityType == 'outdegree':
		return list(nx.out_degree_centrality(G).values())
	elif centralityType == 'degree':
		return list(nx.degree_centrality(G).values())
	elif centralityType == 'eigenvector':
		return list(nx.eigenvector_centrality(G).values())
		# The regular eigenvector_centrality() gives error when equal largest magnitude
	elif centralityType == 'closeness':
		return list(nx.closeness_centrality(G).values())
	elif centralityType == 'betweenness':
		return list(nx.betweenness_centrality(G).values())

# Result: get a df with only the users. Go through edges dict to keep only specified users too
def __filterClosedNetwork__(df,column,keepList):
	newDf = df.copy()
	newDf[column] = newDf[column].apply(__filterDict__,keepList=keepList)
	return newDf

def __filterDict__(currLinkDict,keepList):
	newLinkDict = dict()

	# If the dictionary is empty, keep it empty
	if hasattr(currLinkDict,'items') == 0:
		return newLinkDict

	# Go through every key in the dictionary, if the 'TO' field has someone in the keep list, copy that key and val over to the new dictionary
	keyList = list(currLinkDict.keys())
	newLinkDict = {key: currLinkDict[key] for key in keyList if (key[0] in keepList and key[1] in keepList)}
	return newLinkDict

def __calcLabels__(G,labelList):
	labels = {username: username for username in G.nodes() if username in labelList}
	return labels

########## PUBLIC

def removeUsers(df,removalList,strictFilterCol=None):
	if strictFilterCol == None:
		newDf = df[~df.username.isin(removalList)]
		return newDf
	else:
		# To strictly remove all mention of certain users, we could also create an exclusive network of users excluding them.
		edgesDict = mergeDictCol(df[strictFilterCol])
		G = nx.DiGraph()
		G.add_edges_from(edgesDict)
		nodes = G.nodes()

		fullList = list(nodes)	# Get full list of all users in network!
		keepList = [user for user in fullList if user not in removalList]
		newDf = keepOnlyUsers(df,keepList,strictFilterCol=strictFilterCol)
		return newDf

def keepOnlyUsers(df,keepList,strictFilterCol=None):
	if strictFilterCol == None:
		newDf = df[df.username.isin(keepList)]
		return newDf
	else:
		newDf = __filterClosedNetwork__(df,strictFilterCol,keepList)
		isolates = listIsolates(newDf,strictFilterCol,exceptedList=keepList)
		newDf = newDf[~newDf.username.isin(isolates)]
		return newDf

# Anyone mentioned/ followed is NOT an isolate. Only posters possible.
# Remove all isolated users EXCEPT for the users we list that we want to keep.
def listIsolates(df,columnName,exceptedList=None):
	dictList = list(df[columnName])
	userList = list(df['username'])
	isolateList = [userList[i] for i in range(len(dictList)) if dictList[i] == {} and userList[i] not in exceptedList]
	return isolateList

# Top users of whole network
def listTopCentralityUsers(df,columnName,numUsers=None,centralityType='degree'):
	if numUsers == None: numUsers = len(df[columnName])

	edgesDict = mergeDictCol(df[columnName])

	G = nx.DiGraph()
	G.add_edges_from(edgesDict)	# Determines the order of edges. Will add new nodes in order.
	nodes = G.nodes()

	centrality = __calcCentrality__(G,centralityType)
	centralityDf = pd.DataFrame()
	centralityDf['username'] = nodes
	centralityDf['centrality'] = centrality

	# This gets us a df of ALL the users in the network, not just posting
	newDf = pd.merge(centralityDf,df,on='username',how='outer')
	newDf = newDf.sort_values(by=['centrality'],ascending=False)
	listTopUsers = list(newDf.iloc[0:numUsers]['username'])

	return listTopUsers

def drawGraph(df,columnName,title=None,removeIsolates=False,labelList=None,colorDict=None,minSize=20,sizesDict=None,sizeScale=100,edgesDict=None,widthScale=1,edgeAlpha=0.5,block=True,saveAndClose=False):

	nodes = list(df['username'])
	edges = mergeDictCol(df[columnName])

	plt.figure(figsize=[10, 8])
	G = nx.DiGraph()
	G.add_nodes_from(nodes)	# Can't just rely on edges because of 'reply_to' network where there are people in the network that post but don't reply to anyone in particular
	G.add_edges_from(edges)

	if removeIsolates: G.remove_nodes_from(list(nx.isolates(G)))

	pos = nx.spring_layout(G,k=0.2,iterations=20)

	labels = None
	nodeColors = None
	nodeSizes = None
	edgeWidths = None

	if labelList is not None: labels = __calcLabels__(G,labelList)
	if colorDict is not None: nodeColors = __calcColors__(G,colorDict)
	if sizesDict is not None: nodeSizes = __calcSizes__(G,sizesDict,sizeScale,minSize=minSize)
	if edgesDict is not None:
		edgeWidths = __calcEdgeWidth__(G,edgesDict,widthScale)
	else:
		edgeWidths = __calcEdgeWidth__(G,edges,widthScale)

	nx.draw_networkx_nodes(G,pos,G.nodes(),node_color=nodeColors,node_size=nodeSizes)
	nx.draw_networkx_edges(G,pos,G.edges(),width=edgeWidths,alpha=edgeAlpha)
	if labels is not None: nx.draw_networkx_labels(G,pos,labels)

	plt.axis('off')
	plt.title(title,fontweight='bold')
	plt.tight_layout()
	plt.show(block=block)

	if saveAndClose == True:
		plt.savefig(title+'.jpg')
		plt.close()

def mergeDictCol(dfColumn):
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


