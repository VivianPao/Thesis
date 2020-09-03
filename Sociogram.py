
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
from collections import ChainMap

# Sentiment constants
H_CUTOFF = 0.05
L_CUTOFF = -0.05
POS = 2
NEU = 1
NEG = 0

# Centrality calc constants
IN_CEN = 0
OUT_CEN = 1
EIG_CEN = 2
CLOSE_CEN = 3
BTWN_CEN = 4

IN_DEG_CEN = 0
OUT_DEG_CEN = 1
DEG_CEN = 2
EIG_CEN = 3
CLOSE_CEN = 4
BTWN_CEN = 5

OUT_MIN = 50
OUT_MAX = 600

class Sociogram:

	def __init__(self,twintDf):
		# Get only the required data from the dataframe
		self.nodes = self.calcNodes(twintDf)
		[self.edges,self.edgeWeights] = self.calcEdges(twintDf)
		self.sentiment = list(twintDf['sentiment'])

		# Set up graph
		self.G = nx.DiGraph()
		self.G.add_nodes_from(self.nodes)	# By adding nodes first, we fix the order for usernames we know of already.
		self.G.add_edges_from(self.edges)	# Determines the order of edges. Will add new nodes in order.

	def calcFeatures(self,topN,centralityType):
		nodes = list(self.G.nodes())	# Save updated node list. Includes other mentioned users from edges
		self.edgeWidths = [weight*0.5 for weight in self.edgeWeights]

		# Calculate node size using centrality
		centrality = self.calcCentrality(centralityType)
		inMin = min(centrality)	# Map min, max centrality values for desired node size
		inMax = max(centrality)
		self.nodeSizes = [(nodeCen-inMin)/(inMax-inMin+0.001)*(OUT_MAX-OUT_MIN)+OUT_MIN for nodeCen in centrality] # +0.001 in case inMax-inMin == 0. Avoid dividing by 0.

		self.nodeColors = self.calcColors(self.sentiment)

		# Labels, which change depending on input
		self.centralityDf = pd.DataFrame({'username': nodes,'centrality': centrality})
		self.centralityDf = self.centralityDf.sort_values(by=['centrality'],ascending=False)
		topNUsers = list(self.centralityDf.iloc[0:topN]['username'])
		self.labels = self.calcLabels(topNUsers)

	def drawNetwork(self):	# Add parameter as option to show minor labels
		# pos = nx.spring_layout(self.G)
		pos = nx.kamada_kawai_layout(self.G)
		# pos = nx.fruchterman_reingold_layout(self.G)
		nx.draw_networkx_nodes(self.G,pos,self.G.nodes(),node_size=self.nodeSizes,node_color=self.nodeColors,edgecolors='k')
		nx.draw_networkx_labels(self.G,pos,self.labels)	# Implement separated label commands for different centrality
		nx.draw_networkx_edges(self.G,pos,self.G.edges(),width=self.edgeWidths)
		plt.show(block=False)

	def calcColors(self,sentiment):	# Given list of sentiment floats, generate list of colors for nodes
		colorList = ['r','y','g','w']
		colorCode = []
		for s in sentiment:
			if s > H_CUTOFF:
				color = POS
			elif s < H_CUTOFF and s > L_CUTOFF:
				color = NEU
			else:
				color = NEG
			colorCode.append(colorList[color])

		nodeColors = np.concatenate((colorCode,['w']*(len(self.G.nodes()) - len(sentiment))))
		return nodeColors

	def calcNodes(self,twintDf):
		nodes = twintDf['username'].tolist()
		return nodes

	def calcEdges(self,twintDf):
		# Retrieve all dictionary items in 'reply_to' column in flat list
		nestedListOfDicts = twintDf['reply_to'].tolist()
		listOfDicts = []
		for i in range(len(nestedListOfDicts)):
			if nestedListOfDicts[i] != {}:
				listOfDicts.append(nestedListOfDicts[i])

		edgeDict = dict(ChainMap(*listOfDicts))	# Merge all dictionaries
		edges = list(edgeDict.keys())
		edgeWeights = list(edgeDict.values())
		return [edges,edgeWeights]

	def calcCentrality(self,centralityType):
		if centralityType == IN_DEG_CEN:
			return list(nx.in_degree_centrality(self.G).values())
		elif centralityType == OUT_DEG_CEN:
			return list(nx.out_degree_centrality(self.G).values())
		elif centralityType == DEG_CEN:
			return list(nx.degree_centrality(self.G).values())
		elif centralityType == EIG_CEN:
			return list(nx.eigenvector_centrality_numpy(self.G).values())
			# The regular eigenvector_centrality() gives error when equal largest magnitude
		elif centralityType == CLOSE_CEN:
			return list(nx.closeness_centrality(self.G).values())
		elif centralityType == BTWN_CEN:
			return list(nx.betweenness_centrality(self.G).values())
		else:	# Set default to in degree centrality
			return list(nx.out_degree_centrality(self.G).values())

	def calcLabels(self,topUsers):
		labels = {} 
		for username in self.G.nodes():
		    if username in topUsers:
		        labels[username] = username
		return labels

	def saveSummary(self,nameCSV):	# Create rank column, put it as first column, then save
		self.centralityDf['rank'] = [rank+1 for rank in range(len(self.centralityDf))]
		self.centralityDf[['rank','username','centrality']].to_csv(nameCSV,index=False)
