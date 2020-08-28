
# Dependencies: twint, numpy, scipy, pandas, matplotlib 3.1, networkx, json, textblob

# Input:
# - Topic string (TOPIC)
# - Number of influential users to identify (TOP_N)
# - Number of tweets to scrape (TWEET_LIM)
# - Flags on whether to show the names of minor users on the visualisation (SHOW_MINOR_LABELS) or reuse previously found data (REUSE_DATA)

# Output:
# - SNA visualisation (no meaningful sentiment shown yet so the feature is off by default). The top N nodes are labelled by their rank in the network NOT their username. Their usernames are in info_summary.txt
# - info_summary.txt: lists top N users in descending order of influence
# - Several JSON files that save the scraped data so that the network can be visualised again without new data scraping

# First, run the code with 'REUSE_DATA = False' to prompt the code to find new data. The code will produce a visualisation and a summary of the top users. It also produces a number of JSON files saving the data collected.
# If you want to run the code again for the SNA visualisation or to specify a different TOP_N of users using the same data, switch the REUSE_DATA flag to True. The JSON files from the previous run will be read.

# We currently use degree centrality (in + out) as measure of influence.
# Sentiment analysis is unreliable and will be improved soon.
# ---------------------------------------------------------------

import matplotlib.pyplot as plt
import networkx as nx
import json

from twitterScraping import *
from dataManipulation import *
from sentimentAnalysis import *

# ***************************************************************
# USER INPUTS
# ***************************************************************
TOPIC = "western sydney airport"
TWEET_LIM = 100				# The number of tweets to scrape from Twitter before stopping.
TOP_N = 50					# How many major users to identify. If TOP_N = 10, code names top 10 users.

REUSE_DATA = False 			# If true, the code will look for previously created JSON files from the first scrape
SHOW_MINOR_LABELS = False	# If true, less significant users will also be labelled.

# ***************************************************************
# ADVANCED INPUTS
# ***************************************************************
# Constants
ASSESS_LIM = 20
MAJOR_LABEL_SIZE = 12
MINOR_LABEL_SIZE = 5
COLOR_POS = 'g'
COLOR_NEU = 'y'
COLOR_NEG = 'r'
COLOR_DEFAULT = 'w'

# Features currently in development
SHOW_SENTIMENT = False		# If true, the code will take a long time to search for tweets for the top N users
MANUAL_SENTIMENT = False 	# If true, reads a file indicating each user's sentiment that we prepare beforehand. Keep false for now.

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
	# with open('majorTweets.json', 'r') as f:
	#     majorTweets = json.load(f)	# Dict
	with open('manualSentiment.json', 'r') as f:
	    manualSentiment = json.load(f)	# Dict

else:
	# If we are getting fresh data, we cannot do manual sentiment at the same time
	MANUAL_SENTIMENT = False

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
pos = nx.kamada_kawai_layout(G) # positions for all nodes... Adds a lot of time
# pos = nx.spring_layout(G) # Faster, less insightful layout

# ***************************************************************
# CALCULATING IMPORTANT FEATURES
# ***************************************************************
centralityMeasure = list(nx.degree_centrality(G).values())	# Calculate the node sizes and line widths
topIndices = findTopNindices(centralityMeasure,TOP_N)	# Find the node indices corresponding to the top N users

# Find tweets of major users
# if REUSE_DATA == False and SHOW_SENTIMENT == True:
# 	majorTweets = {}	# Gets filled later in "NODE COLOR" when we search for sentiment
# 	for i in topIndices:
# 		name = nodes[i]
# 		tweets = getTweetsFrom(name,TOPIC,ASSESS_LIM)
# 		majorTweets[name] = tweets

# Print names and in/ out degree of major users
inDegree = list(nx.in_degree_centrality(G).values())
outDegree = list(nx.out_degree_centrality(G).values())
stringTopN = ""
for rank in range(len(topIndices)):
	index = topIndices[rank]
	name = nodes[index]
	stringTopN = stringTopN + str(rank+1)+". "+str(name)+"\n"
	# stringTopN = stringTopN + str(round(inDegree[index],4)) +"/"+ str(round(outDegree[index],4))+"\n"
print(stringTopN)

# ***************************************************************
# SAVE ALL DATA
# ***************************************************************
if REUSE_DATA == False:

	with open("nodes.json", "w") as f:
	    json.dump(nodes,f)
	with open("edges.json", "w") as f:
	    json.dump(edges,f)
	with open("edgeWeight.json", "w") as f:
	    json.dump(list(edgesDict.values()),f)	# Edge weight that gets calculated again later

	# if SHOW_SENTIMENT == True:
	# 	with open("majorTweets.json", "w") as f:
	# 	    json.dump(majorTweets,f)

	# Create template JSON for manual sentiment
	manualSentiment = {}
	for i in topIndices:
		name = nodes[i]
		manualSentiment[name] = 0	# Neutral sentiment to start with
	with open("manualSentiment.json", "w") as f:
	    json.dump(manualSentiment,f)

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
rank = 1
for i in topIndices:
	name = nodes[i]
	majorLabels[name] = rank#name
	rank += 1

# NODE COLOR - Find sentiment of the major users and set the appropriate node color
nodeColor = []
if SHOW_SENTIMENT == True:
	nodeColor = [COLOR_DEFAULT] * len(nodes)	# Make all nodes default color to start

	for i in topIndices:
		name = nodes[i]

		if MANUAL_SENTIMENT == True:
			userSentiment = manualSentiment[name]	# dictionary[name] = 1,0, or -1 for sentiment.
		else:
			userTweets = majorTweets[name]
			userSentiment = calcUserSentiment(userTweets)

		# Make node the appropriate colour to show sentiment
		if userSentiment == 0:
			nodeColor[i] = COLOR_NEU
		elif userSentiment > 0:
			nodeColor[i] = COLOR_POS
		else:
			nodeColor[i] = COLOR_NEG
		print(name,userSentiment,nodeColor[i])

# ***************************************************************
# DRAW SOCIGRAM & SAVE FIGURES
# ***************************************************************
f = plt.figure()
plt.axis('off')
plt.title(TOPIC.title(),fontweight="bold")

nx.draw_networkx_edges(G, pos, G.edges(),width=edgeWeight,alpha=0.6)
nx.draw_networkx_nodes(G, pos, G.nodes(),node_size=nodeSizes,edgecolors='k',node_color=nodeColor)
nx.draw_networkx_labels(G, pos, labels=majorLabels, font_size=MAJOR_LABEL_SIZE,font_weight='bold',font_color='k')

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

# TO VIVIAN:
# git checkout experiment_branch
# source sna_env/bin/activate
# TO DO:
# - Add time frame in which to scrape data: since and until
# - Fix sentiment analysis
# - Add option to select type of centrality used to identify influential users
