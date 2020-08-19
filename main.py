
# CHECKOUT BRANCH
# SOURCE THE VIRTUAL ENV

# Dependencies: numpy, scipy, pandas, matplotlib, networkx, json

# TO DO:
# Add time frame in which to scrape data: since and until
# Fix sentiment analysis
# ---------------------------------------------------------------

import matplotlib.pyplot as plt
import networkx as nx
import json

from twitterScraping import *
from dataManipulation import *
from sentimentAnalysis import *

# User Input
TOPIC = "western sydney airport"
REUSE_DATA = True
SHOW_SENTIMENT = True
SHOW_MINOR_LABELS = False

# Constants
TWEET_LIM = 10000
ASSESS_LIM = 20
TOP_N = 10
MAJOR_LABEL_SIZE = 12
MINOR_LABEL_SIZE = 5
COLOR_POS = 'r'
COLOR_NEU = 'y'
COLOR_NEG = 'g'
COLOR_DEFAULT = 'w'

# ***************************************************************
# TWITTER SCRAPING
# ***************************************************************
# Getting Twint values
if REUSE_DATA == True:
	with open('nodes.json', 'r') as f:
	    nodes = json.load(f)	# List
	with open('edges.json', 'r') as f:
	    edges = json.load(f)	# List
	with open('edgeWeight.json', 'r') as f:
	    edgeWeight = json.load(f)	# List
	with open('majorTweets.json', 'r') as f:
	    majorTweets = json.load(f)	# Dict
else:
	nodesDict = {}
	edgesDict = {}
	nodesDict,edgesDict = findMentioning(TOPIC,TWEET_LIM)
	nodes = list(nodesDict.keys())
	edges = list(edgesDict.keys())

# ***************************************************************
# SOCIOGRAM SET UP
# ***************************************************************
# Setting up the graph
G = nx.MultiDiGraph()
G.add_nodes_from(nodes)	# Determines the order of nodes
G.add_edges_from(edges)	# Determines the order of edges
# pos = nx.kamada_kawai_layout(G) # positions for all nodes... Adds a LOT of time
pos = nx.spring_layout(G) # Faster, less insightful layout

# ***************************************************************
# CALCULATING IMPORTANT FEATURES
# ***************************************************************
centralityMeasure = list(nx.degree_centrality(G).values())	# Calculate the node sizes and line widths
topIndices = findTopNindices(centralityMeasure,TOP_N)	# Find the node indices corresponding to the top N users

# Find tweets of major users
if REUSE_DATA == False and SHOW_SENTIMENT == True:
	majorTweets = {}	# Gets filled later in "NODE COLOR" when we search for sentiment
	for i in topIndices:
		name = nodes[i]
		tweets = getTweetsFrom(name,TOPIC,ASSESS_LIM)
		majorTweets[name] = tweets

# Print names of major users
stringTopN = ""
for rank in range(len(topIndices)):
	index = topIndices[rank]
	name = nodes[index]
	stringTopN = stringTopN + "MAJOR USER "+str(rank+1)+":"+str(name)+"\n"
print(stringTopN)

# Writing details to text file
with open("info_summary.txt", "w") as f:
	summary = "TOPIC: %s\nTWEET_LIM: %d\nASSESS_LIM: %d\nTOP_N: %d\n\n" % (TOPIC,TWEET_LIM,ASSESS_LIM,TOP_N)
	f.write(summary)
with open("info_summary.txt", "a") as f:
	f.write(stringTopN)

# ***************************************************************
# SAVE ALL DATA
# ***************************************************************
if REUSE_DATA == False:
	with open("nodes.json", "w") as f:
	    json.dump(nodes,f)
	with open("edges.json", "w") as f:
	    json.dump(edges,f)
	with open("majorTweets.json", "w") as f:
	    json.dump(majorTweets,f)
	with open("edgeWeight.json", "w") as f:
	    json.dump(list(edgesDict.values()),f)	# Edge weight that gets calculated again later
	
	# Writing details to text file
	with open("info_summary.txt", "w") as f:
		summary = "TOPIC: %s\nTWEET_LIM: %d\nASSESS_LIM: %d\nTOP_N: %d\n\n" % (TOPIC,TWEET_LIM,ASSESS_LIM,TOP_N)
		f.write(summary)
	with open("info_summary.txt", "a") as f:
		f.write(stringTopN)

# ***************************************************************
# CALCULATE VISUAL SOCIOGRAM FEATURES
# ***************************************************************

# NODE SIZE
nodeSizes = [nodeVal*10000 for nodeVal in centralityMeasure]	# Multiply all node sizes by 500 to increase scale

# EDGE WEIGHT
if REUSE_DATA == False:
	edgeWeight = list(edgesDict.values())
edgeWeight = [edgeVal*0.1 for edgeVal in edgeWeight]

# LABELS
majorLabels = {}	# Create a dictionary with only the major node labels
for i in topIndices:
	name = nodes[i]
	majorLabels[name] = name

# NODE COLOR - Find sentiment of the major users and set the appropriate node color
nodeColor = []
if SHOW_SENTIMENT == True:
	nodeColor = [COLOR_DEFAULT] * len(nodes)	# Make all nodes default color to start

	for i in topIndices:	# Go through only the major users, calc sentiment and change color
		userTweets = majorTweets[name]
		userSentiment = calcUserSentiment(userTweets)

		# Make node the appropriate colour to show sentiment
		if userSentiment == 0:
			nodeColor[i] = COLOR_NEU
		elif userSentiment > 0:
			nodeColor[i] = COLOR_POS
		else:
			nodeColor[i] = COLOR_NEG

# ***************************************************************
# DRAW FEATURES & SAVE FIGURES
# ***************************************************************
f = plt.figure()
plt.axis('off')
plt.title(TOPIC.title(),fontweight="bold")

nx.draw_networkx_edges(G, pos, G.edges(),width=edgeWeight,alpha=0.6)
nx.draw_networkx_nodes(G, pos, G.nodes(),node_size=nodeSizes,edgecolors='k',node_color=nodeColor)
nx.draw_networkx_labels(G, pos, labels=majorLabels, font_size=MAJOR_LABEL_SIZE)

f.savefig(TOPIC.title() + " sociogram major.jpg")

# If we want to show minor labels, create dictionary to store them all and adjust size
if SHOW_MINOR_LABELS == True:
	minorLabels = {}	# Create a dictionary with only the major node labels
	for i in range(len(nodes)):
		name = nodes[i]
		if i not in topIndices:
			minorLabels[name] = nodes[i]
	nx.draw_networkx_labels(G, pos, labels=minorLabels, font_size=MINOR_LABEL_SIZE)
	f.savefig(TOPIC.title() + " sociogram all.jpg")

plt.show()
