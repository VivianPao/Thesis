import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import Sociogram
import community as community_louvain
import matplotlib.cm as cm

def drawTop100recipFollowingCommunity(users,tupleFollowers):
	G = nx.DiGraph()
	G.add_nodes_from(users[:100])	# Ensures the top 100 nodes are first in list
	G.add_edges_from(tupleFollowers)
	G = G.to_undirected(reciprocal=True).copy()
	G.remove_nodes_from(list(nx.isolates(G)))

	partition = community_louvain.best_partition(G)

	pos = nx.spring_layout(G)
	# nx.draw_networkx_nodes(G,pos,node_size=20)
	cmap = cm.get_cmap('spring', max(partition.values()) + 1)
	nx.draw_networkx_nodes(G, pos, partition.keys(),
	                       cmap=cmap, node_color=list(partition.values()),edgecolors='gray')

	labels = {} 	# Assign labels only to the top 100 nodes
	for username in list(G.nodes)[:100]:
	    labels[username] = username

	nx.draw_networkx_labels(G,pos,labels,font_size=6,alpha=1)	# Label only the top 100

	nx.draw_networkx_edges(G,pos,width=0.6,alpha=0.4)#0.2)
	plt.axis('off')
	plt.show()


def drawTop100recipFollowingCommunityWColor(users,tupleFollowers,highlightList,color):
	G = nx.DiGraph()
	G.add_nodes_from(users[:100])	# Ensures the top 100 nodes are first in list
	G.add_edges_from(tupleFollowers)
	G = G.to_undirected(reciprocal=True).copy()
	G.remove_nodes_from(list(nx.isolates(G)))

	partition = community_louvain.best_partition(G)
	pos = nx.spring_layout(G)


	colorList = []
	nodeSizeList = []
	nodeEdgeColorList = []
	nodeEdgeWidList = []
	baseNodeSize = 50
	baseNodeEdgeWid = 0.7
	for node in list(G.nodes()):
		if node in highlightList:
			colorList.append(color)
			nodeSizeList.append(baseNodeSize*4)
			nodeEdgeColorList.append('k')
			nodeEdgeWidList.append(baseNodeEdgeWid*4)
		else:
			colorList.append('w')
			nodeSizeList.append(baseNodeSize)
			nodeEdgeColorList.append('w')
			nodeEdgeWidList.append(None)


	# nx.draw_networkx_nodes(G,pos,node_size=20)
	cmap = cm.get_cmap('spring', max(partition.values()) + 1)
	nx.draw_networkx_nodes(G, pos, partition.keys(),
	                       cmap=cmap, node_color=list(partition.values()),edgecolors=nodeEdgeColorList,node_size=nodeSizeList,linewidths=nodeEdgeWidList)


	# nx.draw_networkx_nodes(G, pos, node_color=colorList,edgecolors='gray',node_size=nodeSizeList)

	labels = {} 	# Assign labels only to the top 100 nodes
	for username in highlightList:
		if username in list(G.nodes()):
		    labels[username] = username

	nx.draw_networkx_labels(G,pos,labels,font_size=10,alpha=1)	# Label only the top 100

	nx.draw_networkx_edges(G,pos,width=0.6,alpha=0.4)#0.2)
	plt.axis('off')
	plt.title('Users calling for action in their support networks')
	plt.show()

def drawFollowingCommunity(users,tupleFollowers):
	G = nx.DiGraph()
	G.add_nodes_from(users[:100])	# Ensures the top 100 nodes are first in list
	G.add_edges_from(tupleFollowers)
	G = G.to_undirected(reciprocal=False).copy()
	G.remove_nodes_from(list(nx.isolates(G)))

	partition = community_louvain.best_partition(G)

	pos = nx.spring_layout(G)
	# nx.draw_networkx_nodes(G,pos,node_size=20)
	cmap = cm.get_cmap('rainbow', max(partition.values()) + 1)
	nx.draw_networkx_nodes(G, pos, partition.keys(),
	                       cmap=cmap, node_color=list(partition.values()),edgecolors='gray')

	labels = {} 	# Assign labels only to the top 100 nodes
	for username in list(G.nodes)[:100]:
	    labels[username] = username

	# nx.draw_networkx_labels(G,pos,labels,font_size=6,alpha=1)	# Label only the top 100

	nx.draw_networkx_edges(G,pos,width=0.6,alpha=0.4)#0.2)
	plt.axis('off')
	plt.show()


followerData = pd.read_csv("1-2000.csv")
followerData = followerData[['A','B']]
users = pd.read_csv("allCentrality.csv")	# Ordered by centrality
users = list(users['username'])
topUsers = users[:100]


# Create new dataframe that only contains official users in network
filteredFollowers = followerData[followerData['A'].isin(users) & followerData['B'].isin(users)]
topFilteredFollowers = followerData[followerData['A'].isin(topUsers) & followerData['B'].isin(topUsers)]

tupleFollowers = tuple(zip(filteredFollowers.A, filteredFollowers.B))
topTupleFollowers = tuple(zip(topFilteredFollowers.A, topFilteredFollowers.B))
print(topTupleFollowers)



# usersCallingAction = ['2ser', '33andme', '7NewsSydney', 'AmandaFoxonHill', 'Bas1914', 'Bibittybobitty', 'BlacktownSun', 'Dream_Brother_', 'Fairgoforsolar', 'FrancisYoung2', 'Hotel_Reviewer', 'JeanmLopez', 'JoeHockey', 'JohnBlackTweets', 'KakLinds', 'LeftyLongtitude', 'LevonSib', 'Linny57284055', 'NewtonMark', 'OnlineUKNews', 'Pannawonica', 'PeterTRoberts', 'PlanAssist', 'ScotMacDonald1', 'StephenConry', 'TheSydneyBlog', 'ThumpersAunt', 'alison_rixon', 'araluenvalley', 'australian', 'bambul', 'blacktowncc', 'ebryden4', 'ellinjaa', 'hot_dipper', 'hugh_mcdermott', 'jenstar52', 'lollylegs71', 'lridicol', 'mgdewall', 'michaelkoziol', 'mintomusings', 'muzslyagirl', 'peterjameswills', 'profsarahj', 'taylanicholls', 'timmydownawell', 'wilfrog1968']

# drawTop100recipFollowingCommunity(topUsers,topTupleFollowers)
drawFollowingCommunity(users,tupleFollowers)
# drawTop100recipFollowingCommunityWColor(users,topTupleFollowers,usersCallingAction,'r')

# to repackage the edges as dict for Sociogram input: Column A - remove duplicates. then use as key to choose list to append Column B values to.


# Go through each follower, compare before and after the filtering. 
