
# CHECKOUT BRANCH
# SOURCE THE VIRTUAL ENV

import twint
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from assess_user import *

TOPIC = "western sydney airport"

SHOW_MINOR_LABELS = False
MAJOR_LABEL_SIZE = 12
MINOR_LABEL_SIZE = 5

TWEET_LIM_PER_SEARCH = 10000

TOP_N = 10

# Given an array and a value, delete the first instance of the value from the array
def __deleteElement__(givenArray,givenVal):
	returnArray = []
	for val in givenArray:
		if val is not givenVal:
			returnArray.append(val)
	return returnArray

# Given an array, find the indices of the top n values
def findTopNindices(givenArray,n):
	# If n is larger than the length of the array, set 'n' to the length
	if n > len(givenArray):
		n = len(givenArray)

	# Find indices that give top n values
	topNindices = np.argpartition(givenArray, -n)[-n:]

	# Reorganise indices in descending order
	unordered = list(topNindices)	# Need to make sure you cast as list(). Else it doesn't work
	ordered = []
	for i in range(n):	# Run n times
		maxIndex = unordered[0]
		maxVal = givenArray[maxIndex]
		for index in unordered:
			if givenArray[index] > maxVal:	# If element greater than max stored
				maxVal = givenArray[index]	# Set max to this. Eventually find max in the array.
				maxIndex = index

		ordered.append(maxIndex)
		unordered = __deleteElement__(unordered,maxIndex)

	return ordered

# If the user has been seen before, increment their count. If not, add them into the dictionary and set count to 1.
def addToDict(dictName,keyValue):
	if keyValue not in dictName:
		dictName[keyValue] = 1
	else:
		dictName[keyValue] += 1

# Based on the posts of a topic, find all the users that have mentioned a particular person on a topic (or no topic)
def findMentioning(topic):
	FROM = 0
	TO = 1
	
	c = twint.Config()
	c.Limit = TWEET_LIM_PER_SEARCH
	c.Pandas = True
	c.Search = topic
	c.Format = "{username} | {mentions}"
	twint.run.Search(c)

	collectedData = twint.storage.panda.Tweets_df	# Dataframe of series!
	mentions = collectedData.loc[:,('reply_to')]

	mentionsDict = {}	# Key: edge tuple. Value: weight
	usersDict = {}	# Key: username. Value: How many times appeared
	for row in range(len(mentions)):
		for nthMention in range(TO,len(mentions[row])):	# For each mentioned user, create a new link to the poster
			source = mentions[row][FROM]['username']
			target = mentions[row][nthMention]['username']
			linkTuple = (source,target)

			addToDict(mentionsDict,linkTuple)
			addToDict(usersDict,source)
			addToDict(usersDict,target)

	return (usersDict,mentionsDict)



# TWITTER SCRAPING ***************************************************************
# Getting Twint values
nodesDict = {}
edgesDict = {}
nodesDict,edgesDict = findMentioning(TOPIC)
nodes = list(nodesDict.keys())
edges = list(edgesDict.keys())

# SOCIOGRAM SET UP ***************************************************************
# Setting up the graph
G = nx.MultiDiGraph()
G.add_nodes_from(nodes)	# Determines the order of nodes
G.add_edges_from(edges)	# Determines the order of edges
pos = nx.spring_layout(G) # positions for all nodes

# Calculate the node sizes and line widths
centralityMeasure = list(nx.degree_centrality(G).values())
nodeSizes = [nodeVal*1000 for nodeVal in centralityMeasure]	# Multiply all node sizes by 500 to increase scale
edgeWeight = list(edgesDict.values())
edgeWeight = [edgeVal*2 for edgeVal in edgeWeight]	# Multiply all line widths by 2 to increase scale

# Find the node indices corresponding to the top N users
topIndices = findTopNindices(centralityMeasure,TOP_N)

# LABEL ***************************************************************
# Label only the top N nodes.
majorLabels = {}	# Create a dictionary with only the major node labels... probably don't need to iterate over whole thing.
for i in topIndices:
	name = nodes[i]
	majorLabels[name] = name

# NODE COLOR ***************************************************************
# Find sentiment of the major users and set the appropriate node color
nodeColor = []
for i in range(len(nodes)):
	name = nodes[i]

	# Only for the top n users, look into tweets and find sentiment
	if i in topIndices:
		print("TOP PERSON: ",name)
		tweets = getTweetsFrom(name,TOPIC)
		userSentiment = calcUserSentiment(tweets)

		# Append the appropriate colour to show sentiment
		if userSentiment == 0:
			nodeColor.append('b')
		elif userSentiment > 0:
			nodeColor.append('g')
		else:
			nodeColor.append('r')
	else:
		 nodeColor.append('w')

# DRAW ***************************************************************
# Drawing features
nx.draw_networkx_nodes(G, pos, G.nodes(),node_size=nodeSizes,edgecolors='k',node_color=nodeColor)
nx.draw_networkx_edges(G, pos, G.edges(),width=edgeWeight,alpha=0.6)
nx.draw_networkx_labels(G, pos, labels=majorLabels, font_size=MAJOR_LABEL_SIZE)

# If we want to show minor labels, create dictionary to store them all and adjust size
if SHOW_MINOR_LABELS is True:
	minorLabels = {}	# Create a dictionary with only the major node labels
	for i in range(len(nodes)):
		name = nodes[i]
		if i not in topIndices:
			minorLabels[name] = nodes[i]
	nx.draw_networkx_labels(G, pos, labels=minorLabels, font_size=MINOR_LABEL_SIZE)

plt.axis('off')
plt.show()


"""
Add time frame in which to scrape data: since and until
----------------
COSMETIC:
Find display method that makes arrows go from one to the other
Avoid line collisions

"""
