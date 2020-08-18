
import twint
import matplotlib.pyplot as plt
import networkx as nx

TWEET_LIM_PER_SEARCH = 20
FROM = 0
TO = 1

def addToDict(dictName,keyValue):
	if keyValue not in dictName:
		dictName[keyValue] = 1
	else:
		dictName[keyValue] += 1

# Based on the posts of a topic, find all the users that have mentioned a particular person on a topic (or no topic)
def findMentioning(topic):
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

# Getting Twint values
nodesDict = {}
edgesDict = {}
nodesDict,edgesDict = findMentioning("akatsuki no yona")
nodes = list(nodesDict.keys())
edges = list(edgesDict.keys())

# Setting up the graph
G = nx.MultiDiGraph()
G.add_nodes_from(nodes)	# Determines the order of nodes
G.add_edges_from(edges)	# Determines the order of edges
pos = nx.spring_layout(G) # positions for all nodes

# Calculate the node sizes and line widths
nodeSizes = list(nx.degree_centrality(G).values())
nodeSizes = [nodeVal*500 for nodeVal in nodeSizes]	# Multiply all node sizes by 500 to increase scale
edgeWeight = list(edgesDict.values())
edgeWeight = [edgeVal*2 for edgeVal in edgeWeight]	# Multiply all line widths by 2 to increase scale

# Drawing features
nx.draw_networkx_nodes(G, pos, G.nodes(),node_size=nodeSizes)
nx.draw_networkx_edges(G, pos, G.edges(),width=edgeWeight)
nx.draw_networkx_labels(G, pos)
plt.axis('off')
plt.show()


# Find display method that makes arrows go from one to the other
# Avoid line collisions




