
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
import pandas as pd
from collections import ChainMap
import ast

from twitterScraping import *
from dataManipulation import *
from sentimentAnalysis import *

def calcWeightedEdges(listOfDicts):
	
	weightedEdges = []
	for i in range(len(listOfDicts)):
		# for one dictionary, match key + value in tuple of form (u,v,w), append in list
		currDict = listOfDicts[i]
		keys = list(currDict.keys())
		for key in keys:
			weightedEdges.append(tuple(list(key)+[currDict[key]*0.5]))

	return weightedEdges

# ***************************************************************
# USER INPUTS
# ***************************************************************
TOPIC = "western sydney airport"
TWEET_LIM = 100				# The number of tweets to scrape from Twitter before stopping.
TOP_N = 50					# How many major users to identify. If TOP_N = 10, code names top 10 users.
NEW_DATA = 0

# ***************************************************************
# TWITTER SCRAPING
# ***************************************************************

if NEW_DATA == 1:
	collectedData = scrapeTopic(TOPIC,TWEET_LIM)
	collectedData.to_csv('data.csv',index=False)

	# Prepare list of dicts
	mergedLinks = collectedData['reply_to'].tolist()

else:
	collectedData = pd.read_csv('data.csv')

	# Get values from reply column
	weightedLinks = collectedData['reply_to'].tolist()	# Link of dictionaries
	mergedLinks = []
	for i in range(len(weightedLinks)):		# Reading in the dictionaries from string format
		if len(weightedLinks[i]) > 2:			# If dictionary is not empty, empty looking like "{}"
			mergedLinks.append(ast.literal_eval(weightedLinks[i]))

#############################

weightedEdges = calcWeightedEdges(mergedLinks)
nodes = collectedData['username'].tolist()


G = nx.MultiDiGraph()
G.add_nodes_from(nodes)
G.add_weighted_edges_from(weightedEdges)
pos = nx.kamada_kawai_layout(G)

nx.draw_networkx_nodes(G,pos)
nx.draw_networkx_edges(G,pos,G.edges())

plt.show()

# ***************************************************************
# PRODUCING SOCIOGRAM
# ***************************************************************

# class sociogram:

# 	def __init__(self,nodes,edges):
# 		self.G = nx.MultiDiGraph(nodes,edges)
# 		self.G.add_nodes_from(nodes)	# Determines the order of nodes
# 		self.G.add_edges_from(edges)	# Determines the order of edges
# 		self.pos = nx.kamada_kawai_layout(G) # positions for all nodes...

# 	def calcInfluence():
# 	def calcSentiment(self):
# 	def drawNetwork():
# 		calcNodeSizes() -> centrality after network is given values
# 		calcEdgeWeights() -> from edges imported... in form of (u,v,w)
# 		calcNodeLabels() -> usernames
# 		calcNodeColors() -> based on sentiment
# 		show___()
# 	def saveData():
# 	def calcNodeColors():
# 		calcSentiment()



# TO VIVIAN:
# git checkout experiment_branch
# source sna_env/bin/activate
# TO DO:
# - Add time frame in which to scrape data: since and until
# - Fix sentiment analysis
# - Add option to select type of centrality used to identify influential users
