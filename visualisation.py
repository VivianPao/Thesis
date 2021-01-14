
import pickle
from ast import literal_eval
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
import pandas as pd
import numpy as np
from collections import ChainMap 
import community as community_louvain

REPLIES = 0
FOLLOWS = 1
INVALID = -1

# Constants: Number of characters in a date string
MONTHLY_CHAR = 7
FULL_DATE_CHAR = 19

# Color options for nodes
COMMUNITY = 1
SENTIMENT = 2
ACTION_CALL = 3
NO_COLOR = 4

def drawActivityOverTime(filename,saveAndClose=False,block=False):
	if ".csv" in filename:
		df = pd.read_csv(filename)
	else:
		df = pd.read_json(filename)
	if checkRepliesOrFollows(df) != 'reply_to':
		print("Invalid")
		return

	dateList = list(df['date'])

	monthDict = {}
	for item in dateList:
		for i in range(len(item)//FULL_DATE_CHAR):
			dateStamp =item[i*FULL_DATE_CHAR:(i+1)*FULL_DATE_CHAR]
			month = dateStamp[:MONTHLY_CHAR]
			if month in monthDict: monthDict[month] += 1
			else: monthDict[month] = 1

	xTicks = list(monthDict.keys())
	xTicks.sort()	# Order the date strings
	x = range(len(xTicks))
	y = [monthDict[x] for x in xTicks]	# Get corresponding values in sorted order

	plt.xticks(x,xTicks)
	plt.plot(x,y)
	plt.xlabel("Year/Month")
	plt.ylabel("Number of Posts")
	plt.title("Network Activity Over Time ("+xTicks[0]+" to "+xTicks[-1]+")")

	plt.show(block=block)
	if saveAndClose == True:
		plt.savefig(title+'.jpg')
		plt.close()

def saveSummary(filename,reciprocal=False):
	# print("Producing CSV Summary")
	df = pd.read_csv(filename)
	df = df.drop(df.columns[0], axis=1) # Drop the index column

	columnName = checkRepliesOrFollows(df)
	df[columnName] = df[columnName].apply(turn2LiteralKeysReply)

	# Whole network
	cDf = calcOverallCentrality(df,columnName)
	cDf = cDf.rename(columns={"degree": "degree centrality (within whole network)", "closeness": "closeness centrality (within whole network)","betweenness": "betweenness centrality (within whole network)","overall": "overall centrality (within whole network)"})

	# For communities
	if reciprocal == True:
		commFilename = filename[:-4]+'_communities_reciprocal'+'.pkl'
		subsubtitle = "reciprocal_for_comm"
	else:
		commFilename = filename[:-4]+'_communities_NOT_reciprocal'+'.pkl'
		subsubtitle = " NOT_reciprocal_for_comm"
	commDict,colorDict = loadOrSaveColorDict(commFilename,df,columnName,reciprocal)

	summaryDf = pd.DataFrame({})

	if commDict == {}:
		summaryDf = cDf
	else:
		commNumList = []
		commUserList = []
		for commNum in list(commDict.keys()):
			commUserList = commDict[commNum]
			commNumList = [commNum]*len(commDict[commNum])

			commDf = keepOnlyUsers(df,commUserList,strictFilterCol=columnName)
			commSummaryDf = calcOverallCentrality(commDf,columnName)
			commSummaryDf.insert(1,"community number",commNumList)
			
			summaryDf = summaryDf.append(commSummaryDf,ignore_index=True)

		summaryDf = summaryDf.rename(columns={"degree": "degree centrality (within own community)", "closeness": "closeness centrality (within own community)","betweenness": "betweenness centrality (within own community)","overall": "overall centrality (within own community)"})

		# DO NOT DELETE THE ONES THAT ARE NOT IN COMMON
		summaryDf = pd.merge(summaryDf, cDf, on='username', how='outer')

	sentimentDf = getSentimentDf(df)
	summaryDf = pd.merge(summaryDf, sentimentDf, on='username', how='outer')
	summaryDf.to_csv('Summary_'+subsubtitle+'.csv')

# Calls for action!
def calcActionCalling(text,actionBank):
	text = text.lower()
	score = 0	# Initial action calling score is 0
	if len(text) != 0:
		# Calculate individual string sentiment and then get the average
		for word in actionBank:
			score += text.count(word)
	return score

def actionCallColor(text,actionBank):
	score = calcActionCalling(text,actionBank)
	if score > 0:
		return 'r'
	else:
		return 'gray'

def calcTextSentiment(text,posBank,negBank):
	# Made lowercase for case insensitive search
	text = text.lower()
	sentiment = 0	# Initial sentiment of 0 (neutral)
	if len(text) != 0:
		# Calculate individual string sentiment and then get the average
		for word in posBank:
			sentiment += text.count(word)
		for word in negBank:
			sentiment -= text.count(word)
	return sentiment

def sentimentColor(text,posBank,negBank):
	score = calcTextSentiment(text,posBank,negBank)
	if score < 0:
		return 'r'
	elif score > 0:
		return 'g'
	else:
		return 'y'

def loadWordBank(filename):
	# Load all the negative words
	f = open(filename, "r")
	lines = f.read().split('\n')	# Retrieve every line
	wordBank = [text.lower() for text in lines if ";" not in text and text != ""]	# If the line has a semicolon or has no text, disregard the line
	# Made lowercase for case insensitive search
	f.close()
	return wordBank

def drawCommFromFile(filename,topN,colorRepresents=None,reciprocal=False,saveAndClose=False,block=False):
	
	######################## LOAD THE DATA #######################
	if ".csv" in filename:
		df = pd.read_csv(filename)
	else:
		df = pd.read_json(filename)

	columnName = checkRepliesOrFollows(df)
	if columnName == 'reply_to':
		subtitle = 'Communities Based On Replies, '
		df['reply_to'] = df['reply_to'].apply(turn2LiteralKeysReply)
	elif columnName == 'followings':
		subtitle = 'Communities Based On Follows, '
		df['followings'] = df['followings'].apply(turn2LiteralKeys)

	######################## LOAD COMMUNITY FILE OR MAKE ONE #######################
	if reciprocal == True:
		commFilename = filename[:-4]+'_communities_reciprocal'+'.pkl'
		subsubtitle = ' reciprocal'
	else:
		commFilename = filename[:-4]+'_communities_NOT_reciprocal'+'.pkl'
		subsubtitle = ' not reciprocal'
	commDict,colorDict = loadOrSaveColorDict(commFilename,df,columnName,reciprocal)

	######################## OVERWRITE COLOR DICTIONARY WITH SELECTION ########################
	subsubtitle = " "
	if columnName == 'reply_to' and colorRepresents == SENTIMENT:
		colorDict = getSentimentColorDict(df)
		subsubtitle = ' Sentiment'
	elif columnName == 'reply_to' and colorRepresents == ACTION_CALL:
		colorDict = getActionCallColorDict(df)
		subsubtitle = ' Action calls'
	elif colorRepresents == NO_COLOR:
		colorDict = None

	######################## DRAW EACH COMMUNITY SEPARATELY ########################
	for i in range(len(commDict)):
		commList = commDict[i]
		commDf = keepOnlyUsers(df,commList,strictFilterCol=columnName)
		cDf = calcOverallCentrality(commDf,columnName)
		overallCenDict = dict(zip(list(cDf['username']),list(cDf['overall'])))
		overallSorted = cDf.sort_values(by='overall',ascending=False)
		labelList = list(overallSorted['username'])
		labelList = labelList[:topN]

		drawGraph(commDf,columnName,title=filename+'- '+subtitle+subsubtitle+'('+str(i)+') ',colorDict=colorDict,sizesDict=overallCenDict,labelList=labelList,sizeScale=100,removeIsolates=False,edgeAlpha=0.05,block=block,saveAndClose=saveAndClose)

def getActionCallColorDict(df):
	actionList = loadWordBank('action-words.txt')
	df['actionCount'] = df['tweet'].apply(actionCallColor,actionBank=actionList)
	colorDict = dict(zip(list(df['username']),list(df['actionCount'])))
	return colorDict

def loadOrSaveColorDict(commFilename,df,columnName,reciprocal):
	# print(df)
	try:
		commDict,colorDict = pd.read_pickle(commFilename)
	except:
		# print(df[columnName])
		# print(columnName)
		# print("Generating communities for first time based on: "+filename)
		commDict = extractCommunities(df,columnName,reciprocal=reciprocal)
		# print("*****************************************")
		if commDict == {}: colorDict = None
		else: colorDict = assignCommunityColors(commDict)

		# Save all community data (blank or filled) into pickle file
		f = open(commFilename,"wb")
		pickle.dump([commDict,colorDict],f)
		f.close()

	if commDict == {}:
		print("No communities found!")

	return [commDict,colorDict]

def getSentimentDf(df):
	posList = loadWordBank('positive-words.txt')
	negList = loadWordBank('negative-words.txt')
	df['sentiment score'] = df['tweet'].apply(calcTextSentiment,posBank=posList,negBank=negList)
	return df[['username','sentiment score']]

def getSentimentColorDict(df):
	posList = loadWordBank('positive-words.txt')
	negList = loadWordBank('negative-words.txt')
	df['sentiment'] = df['tweet'].apply(sentimentColor,posBank=posList,negBank=negList)
	colorDict = dict(zip(list(df['username']),list(df['sentiment'])))
	return colorDict

def drawWholeNetworkFromFile(filename,topN,colorRepresents=None,reciprocal=False,saveAndClose=False,block=False):
	######################## LOAD THE DATA #######################
	if ".csv" in filename:
		df = pd.read_csv(filename)
	else:
		df = pd.read_json(filename)

	columnName = checkRepliesOrFollows(df)
	if columnName == 'reply_to':
		subtitle = 'Replies.'
		df['reply_to'] = df['reply_to'].apply(turn2LiteralKeysReply)

	elif columnName == 'followings':
		subtitle = 'Follows, '
		df['followings'] = df['followings'].apply(turn2LiteralKeys)

	######################## PROCESS AND VISUALISE #######################
	subsubtitle = ' '

	if columnName == 'reply_to' and colorRepresents == SENTIMENT:
		colorDict = getSentimentColorDict(df)
		subsubtitle = ' Sentiment'
	elif columnName == 'reply_to' and colorRepresents == ACTION_CALL:
		colorDict = getActionCallColorDict(df)
		subsubtitle = ' Action calls'
	elif colorRepresents == COMMUNITY:
		if reciprocal == True:
			commFilename = filename[:-4]+'_communities_reciprocal'+'.pkl'
			subsubtitle = " Color: communities, reciprocal"
		else:
			commFilename = filename[:-4]+'_communities_NOT_reciprocal'+'.pkl'
			subsubtitle = " Color: communities, NOT reciprocal"
		commDict,colorDict = loadOrSaveColorDict(commFilename,df,columnName,reciprocal)
	elif colorRepresents == NO_COLOR:
		colorDict = None

	cDf = calcOverallCentrality(df,columnName)
	overallCenDict = dict(zip(list(cDf['username']),list(cDf['overall'])))
	overallSorted = cDf.sort_values(by='overall',ascending=False)
	labelList = list(overallSorted['username'])
	labelList = labelList[:topN]

	drawGraph(df,columnName,title=filename+'- '+subtitle+subsubtitle,colorDict=colorDict,sizesDict=overallCenDict,labelList=labelList,sizeScale=100,minSize=10,removeIsolates=False,edgeAlpha=0.05,block=block,saveAndClose=saveAndClose)


def drawEgoFromFile(filename,user,colorRepresents=None,reciprocal=False,saveAndClose=False,block=False):

	######################## LOAD THE DATA #######################
	if ".csv" in filename:
		df = pd.read_csv(filename)
	else:
		df = pd.read_json(filename)

	columnName = checkRepliesOrFollows(df)
	if columnName == 'reply_to':
		titleTo = 'Egocentric: Who replies to '+user+'.'
		titleFrom = 'Egocentric: Who '+user+' replies to.'
		df['reply_to'] = df['reply_to'].apply(turn2LiteralKeysReply)
	elif columnName == 'followings':
		titleTo = 'Egocentric: Who follows '+user+'.'
		titleFrom = 'Egocentric: Who '+user+' follows.'
		df['followings'] = df['followings'].apply(turn2LiteralKeysReply)
	######################## PROCESS DATA AND VISUALISE ########################
	subsubtitle = ' '
	if columnName == 'reply_to' and colorRepresents == SENTIMENT:
		colorDict = getSentimentColorDict(df)
		subsubtitle = ' Color: Sentiment'
	elif columnName == 'reply_to' and colorRepresents == ACTION_CALL:
		colorDict = getActionCallColorDict(df)
		subsubtitle = ' Color: Action calls'
	elif colorRepresents == COMMUNITY:
		if reciprocal == True:
			commFilename = filename[:-4]+'_communities_reciprocal'+'.pkl'
			subsubtitle = " Color: communities, reciprocal"
		else:
			commFilename = filename[:-4]+'_communities_NOT_reciprocal'+'.pkl'
			subsubtitle = " Color: communities, NOT reciprocal"
		commDict,colorDict = loadOrSaveColorDict(commFilename,df,columnName,reciprocal)
	elif colorRepresents == NO_COLOR:
		colorDict = None

	egoDf = getEgocentricDf(df,columnName,user)
	ego_to = egoDf.loc[egoDf['username'] != user]
	ego_from = egoDf.loc[egoDf['username'] == user]

	# INCOMING CONNECTIONS
	drawGraph(ego_to,columnName,title=titleTo+subsubtitle,block=block,colorDict=colorDict,minSize=10,sizesDict={user:3},labelList=list(egoDf['username'])+[user],edgeAlpha=0.1,saveAndClose=saveAndClose)

	# OUTGOING CONNECTIONS
	edgeDict = mergeDictCol(egoDf[columnName])
	edgeList = list(edgeDict.keys())
	labelList = [edge[1] for edge in edgeList]	# Retrieve the 'to'
	drawGraph(ego_from,columnName,title=titleFrom+subsubtitle,block=block,colorDict=colorDict,minSize=10,sizesDict={user:3},labelList=labelList+[user],edgeAlpha=0.1,saveAndClose=saveAndClose)

######################## FUNCTIONS #######################
def checkRepliesOrFollows(fileDf):
	headingsList = list(fileDf.columns)
	if 'reply_to' in headingsList: return 'reply_to'
	elif 'followings' in headingsList: return 'followings'
	else: return 'INVALID'

def calcOverallCentrality(df,columnName):
	edgeDict = mergeDictCol(df[columnName])
	G = nx.Graph()
	G.add_edges_from(edgeDict)

	centralityDf = pd.DataFrame()
	centralityDf['username'] = list(G.nodes())
	centralityDf['degree'] = __calcCentrality__(G,centralityType='degree')
	# centralityDf['eigenvector'] = __calcCentrality__(G,centralityType='eigenvector')
	centralityDf['closeness'] = __calcCentrality__(G,centralityType='closeness')
	centralityDf['betweenness'] = __calcCentrality__(G,centralityType='betweenness')

	# print(centralityDf)
 
	if (max(list(centralityDf['degree'])) != min(list(centralityDf['degree']))):
		centralityDf['degree'] = (centralityDf['degree'] - min(list(centralityDf['degree'])))/(max(list(centralityDf['degree']))-min(list(centralityDf['degree'])))
	# centralityDf['eigenvector'] = (centralityDf['eigenvector'] - min(list(centralityDf['eigenvector'])))/(max(list(centralityDf['eigenvector']))-min(list(centralityDf['eigenvector'])))
	if (max(list(centralityDf['closeness'])) != min(list(centralityDf['closeness']))):
		centralityDf['closeness'] = (centralityDf['closeness'] - min(list(centralityDf['closeness'])))/(max(list(centralityDf['closeness']))-min(list(centralityDf['closeness'])))
	if (max(list(centralityDf['betweenness'])) != min(list(centralityDf['betweenness']))):
		centralityDf['betweenness'] = (centralityDf['betweenness'] - min(list(centralityDf['betweenness'])))/(max(list(centralityDf['betweenness']))-min(list(centralityDf['betweenness'])))

	centralityDf['overall'] = centralityDf['degree'] + centralityDf['closeness'] + centralityDf['betweenness'] #+ centralityDf['eigenvector'] 

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
	print(numGroups)
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
def extractCommunities(df,columnName,reciprocal=False,individualsAsCommunities=False):

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
		# print("\nNo communities found :(\n")
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

def drawGraph(df,columnName,title=None,removeIsolates=False,labelList=None,colorDict=None,minSize=20,sizesDict=None,sizeScale=100,edgesDict=None,widthScale=1,edgeAlpha=0.5,block=False,saveAndClose=False):

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

	if colorDict is not None:
		nodeColors = __calcColors__(G,colorDict)
	else:
		nodeColors = 'gray'	# If no color dictionary specified, set nodes to gray

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
