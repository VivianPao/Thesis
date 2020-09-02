
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
from collections import ChainMap

class Sociogram:

	def __init__(self,twintDf):

		# Get only the required data from the dataframe
		self.nodes = self.calcNodes(twintDf)
		[self.edges,self.edgeWeights] = self.calcEdges(twintDf)
		self.sentiment = list(twintDf['sentiment'])

		# Set up graph
		self.G = nx.MultiDiGraph()
		self.G.add_nodes_from(self.nodes)	# By adding nodes first, we fix the order for usernames we know of already.
		self.G.add_edges_from(self.edges)	# Determines the order of edges. Will add new nodes in order.

	def calcFeatures(self,topN):

		nodes = list(self.G.nodes())			# Save updated node list. Includes other mentioned users from edges
		centrality = list(nx.degree_centrality(self.G).values())
		self.edgeWidths = [weight*0.5 for weight in self.edgeWeights]
		self.nodeSizes = [nodeCen*10000 for nodeCen in centrality]
		self.nodeColors = self.calcColors(self.sentiment)

		# Labels, which change depending on input
		self.centralityDf = pd.DataFrame({'username': nodes,'centrality': centrality})
		self.centralityDf = self.centralityDf.sort_values(by=['centrality'],ascending=False)
		topNUsers = list(self.centralityDf.iloc[0:topN]['username'])
		self.labels = self.calcLabels(topNUsers)

	def drawNetwork(self,topN):	# Add parameter as option to show minor labels

		self.calcFeatures(topN)

		pos = nx.spring_layout(self.G) # nx.kamada_kawai_layout(self.G)
		nx.draw_networkx_nodes(self.G,pos,self.G.nodes(),node_size=self.nodeSizes,node_color=self.nodeColors,edgecolors='k')
		nx.draw_networkx_labels(self.G,pos,self.labels)	# Implement separated label commands for different centrality
		nx.draw_networkx_edges(self.G,pos,self.G.edges(),width=self.edgeWidths)
		plt.show()

	def calcColors(self,sentiment):	# Given list of sentiment floats, generate list of colors for nodes
		H_CUTOFF = 0.05
		L_CUTOFF = -0.05
		POS = 2
		NEU = 1
		NEG = 0

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

	def calcLabels(self,topUsers):
		labels = {} 
		for username in self.G.nodes():
		    if username in topUsers:
		        labels[username] = username
		return labels

	def saveSummary(self,nameCSV):	# Create rank column, put it as first column, then save
		self.centralityDf['rank'] = [rank+1 for rank in range(len(self.centralityDf))]
		self.centralityDf[['rank','username','centrality']].to_csv(nameCSV,index=False)
