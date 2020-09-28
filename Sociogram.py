
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
from collections import ChainMap
from networkx.algorithms.community import greedy_modularity_communities
import community as community_louvain
import matplotlib.cm as cm

[IN_DEG_CEN,OUT_DEG_CEN,DEG_CEN,EIG_CEN,CLOSE_CEN,BTWN_CEN] = range(0,6)
CENTRALITY = {'in degree':IN_DEG_CEN,'out degree':OUT_DEG_CEN,'degree':DEG_CEN,'eigenvector':EIG_CEN,'closeness':CLOSE_CEN,'betweenness':BTWN_CEN}

# Sentiment constants
H_CUTOFF = 0#0.05
L_CUTOFF = 0#-0.05
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

	def __init__(self,twintDf,title,topN,centralityType):
		# Get only the required data from the dataframe
		self.df = twintDf
		self.nodes = self.calcNodes(twintDf)
		[self.edges,self.edgeWeights] = self.calcEdges(twintDf)
		self.sentiment = list(self.df['sentiment'])

		# Set up graph
		self.G = nx.DiGraph()
		self.G.add_nodes_from(self.nodes)	# By adding nodes first, we fix the order for usernames we know of already.
		self.G.add_edges_from(self.edges)	# Determines the order of edges. Will add new nodes in order.

		# Compute features and visualise the network
		self.calcFeatures(topN,CENTRALITY[centralityType])

	def calcFeatures(self,topN,centralityType):
		nodes = list(self.G.nodes())	# Save updated node list. Includes other mentioned users from edges

		self.edgeWidths = None
		if len(self.edges) != 0:
			self.edgeWidths = [weight*0.5 for weight in self.edgeWeights]
			self.edgeWidths = (self.edgeWidths-np.min(self.edgeWidths))/(np.max(self.edgeWidths)-np.min(self.edgeWidths)+0.001)*3 + 1
			self.edgeWidths = self.edgeWidths/self.edgeWidths

		self.nodeColors = self.calcColors(self.sentiment)

		# Calculate node size using centrality
		centrality = self.calcCentrality(self.G,centralityType)
		inMin = min(centrality)	# Map min, max centrality values for desired node size
		inMax = max(centrality)
		self.nodeSizes = [(nodeCen-inMin)/(inMax-inMin+0.001)*(OUT_MAX-OUT_MIN)+OUT_MIN for nodeCen in centrality] # +0.001 in case inMax-inMin == 0. Avoid dividing by 0.

		# Labels, which change depending on input
		# Add centrality column to the df
		centralityDf = pd.DataFrame({'username': nodes,'centrality': centrality})
		self.df = pd.merge(self.df,centralityDf,on='username')
		self.df = self.df.sort_values(by=['centrality'],ascending=False)
		# print(self.df['centrality'])
		topNUsers = list(self.df.iloc[0:topN]['username'])
		self.labels = self.calcLabels(topNUsers)

	def drawNetwork(self,title,showSentiment=False):	# Add parameter as option to show minor labels
		plt.figure(figsize=[10, 8])

		pos = nx.spring_layout(self.G)
		# pos = nx.kamada_kawai_layout(self.G)
		# pos = nx.fruchterman_reingold_layout(self.G)
		if showSentiment:
			nx.draw_networkx_nodes(self.G,pos,self.G.nodes(),node_size=self.nodeSizes,node_color=self.nodeColors,edgecolors='gray')
		else:
			nx.draw_networkx_nodes(self.G,pos,self.G.nodes(),node_size=self.nodeSizes,edgecolors='gray')
			
		nx.draw_networkx_labels(self.G,pos,self.labels)	# Implement separated label commands for different centrality
		nx.draw_networkx_edges(self.G,pos,self.G.edges(),width=self.edgeWidths)

		# Create figure and save as image
		plt.axis('off')
		plt.title(title,fontweight='bold')
		plt.tight_layout()
		# plt.savefig(title + ' sociogram.jpg')
		# plt.show(block=False)

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

	def calcCentrality(self,G,centralityType=DEG_CEN):
		if centralityType == IN_DEG_CEN:
			return list(nx.in_degree_centrality(G).values())
		elif centralityType == OUT_DEG_CEN:
			return list(nx.out_degree_centrality(G).values())
		elif centralityType == DEG_CEN:
			return list(nx.degree_centrality(G).values())
		elif centralityType == EIG_CEN:
			return list(nx.eigenvector_centrality_numpy(G).values())
			# The regular eigenvector_centrality() gives error when equal largest magnitude
		elif centralityType == CLOSE_CEN:
			return list(nx.closeness_centrality(G).values())
		elif centralityType == BTWN_CEN:
			return list(nx.betweenness_centrality(G).values())
		else:	# Set default to in degree centrality
			return list(nx.out_degree_centrality(G).values())

	def calcLabels(self,topUsers):
		labels = {} 
		for username in self.G.nodes():
		    if username in topUsers:
		        labels[username] = username
		return labels

	def saveSummary(self,nameCSV):	# Create rank column, put it as first column, then save
		# self.savedDf['in degree'] = 
		# self.savedDf['out degree'] = 

		# Add centrality ranking to the dataframe
		savedDf = self.df.copy()
		savedDf['rank'] = [rank+1 for rank in range(len(self.df))]
		savedDf[['rank','username']].to_csv(nameCSV,index=False)
		# 'rank','username','in degree','out degree'
		
		# self.sentiment
		# 	Count how many terms +ve, -ve, 0

	def getTopNDf(self,topN):
		# Don't share the centrality values
		if topN < len(self.df.index):
			tempDf = self.df.iloc[0:topN]
			return tempDf.loc[:,self.df.columns != 'centrality']
		else:
			return self.df.loc[:,self.df.columns != 'centrality']

	def drawCommunities(self,reciprocal=False):
		colors = ['r','orange','b','c','g','y','m','pink']
		G = self.G.to_undirected(reciprocal=reciprocal).copy()
		G.remove_nodes_from(list(nx.isolates(G)))
		communities = greedy_modularity_communities(G)

		for c in range(len(communities)):
			plt.figure(figsize=[10, 8])
			subG = G.subgraph(communities[c]).copy()
			pos = nx.spring_layout(subG,k=1) # positions for all nodes
			nx.draw_networkx_nodes(subG, pos, subG.nodes(),node_color=colors[c%len(colors)],edgecolors='gray')
			nx.draw_networkx_edges(subG, pos, subG.edges(),edge_color='gray')
			nx.draw_networkx_labels(subG, pos)

			plt.axis('off')

	def drawCommunitiesTogether(self,reciprocal=False):
		# compute the best partition
		plt.figure(figsize=[10, 8])
		G = self.G.to_undirected(reciprocal=reciprocal)
		G.remove_nodes_from(list(nx.isolates(G)))
		partition = community_louvain.best_partition(G)
		pos = nx.spring_layout(G)#,k=1.5)
		# color the nodes according to their partition
		cmap = cm.get_cmap('jet', max(partition.values()) + 1)
		nx.draw_networkx_nodes(G, pos, partition.keys(),
		                       cmap=cmap, node_color=list(partition.values()),edgecolors='gray')
		nx.draw_networkx_edges(G, pos, alpha=0.5)

		topN = 20
		centrality = self.calcCentrality(G)
		centralityDf = pd.DataFrame({'username': list(G.nodes),'centrality': centrality})
		centralityDf = centralityDf.sort_values(by=['centrality'],ascending=False)
		topNUsers = list(centralityDf.iloc[0:topN]['username'])
		labels = {}
		for username in G.nodes():
		    if username in topNUsers:
		        labels[username] = username

		nx.draw_networkx_labels(G,pos,labels)
		# plt.show()

	# def drawReciprocalsOnly(self,removeIsolated=True):
	# 	undirG = self.G.to_undirected(reciprocal=True)

	# 	if removeIsolated:
	# 		undirG.remove_nodes_from(list(nx.isolates(undirG)))

	# 	plt.figure(figsize=[10, 8])
	# 	pos = nx.spring_layout(undirG)

	# 	nx.draw_networkx_nodes(undirG,pos,undirG.nodes(),edgecolors='gray',node_color='orange')
	# 	nx.draw_networkx_labels(undirG,pos)	# Implement separated label commands for different centrality
	# 	nx.draw_networkx_edges(undirG,pos,undirG.edges(),edge_color='gray')

	# 	plt.axis('off')
