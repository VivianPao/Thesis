
import matplotlib.pyplot as plt
import networkx as nx

# NOW:
# Get pos working for graph
# Try calculating centrality for all nodes
# Draw the graph with varying node sizes based on centrality values

# Be careful. Edges MUST have a source and target. And don't self-link, it skews centrality measures
# Make dictionary of edges and iterate through them for each combination with tuple as key. Weight should be the value.
# Make opacity 0.5 so you can see arrows/ links in both directions. (Don't combine them or cover the other)
# print((1,2) == (2,1))	# False. Order is important.

G = nx.MultiDiGraph()
nodes = ["1","3","5","2","4"]
edges = [["1","2"],["3","2"],["4","3"],["1","2"],["1","5"]]

labels = {}	# Create a dictionary with only the major node labels
labels["1"] = 1

G.add_nodes_from(nodes)	# Determines the order of nodes
G.add_edges_from(edges)	# Determines the order of edges

pos = nx.spring_layout(G) # positions for all nodes

print(G.nodes())
print(G.edges())

# Calculate degree centrality of each node and map it to node size
nodeSizes = list(nx.degree_centrality(G).values())
nodeSizes = [nodeVal*500 for nodeVal in nodeSizes]	# Multiply all node sizes by 500 to increase scale
print(nodeSizes)

# CALCULATE IN DEGREE AND OUT DEGREE CENTRALITY AND PRINT OUT.







# Calculate weighting of each edge and map to width of line... direct number is fine
# Store edges as dictionary with tuples (edges) as key, weight as value

# Check if the dictionary behaviour is the same when you use strings as keys/ node names instead
TOPIC = "western sydney airport"
f = plt.figure()
plt.axis('off')
plt.title(TOPIC.title())


nx.draw_networkx_nodes(G, pos, G.nodes(),node_size=nodeSizes, edgecolors='k')
f.savefig(TOPIC.title() + ' sociogram1.jpg')

nx.draw_networkx_edges(G, pos, G.edges(),width=[1,10,3])

# Think of how to change the colour of each node based on sentiment
# Find reasonable way to label only the important nodes... check centrality. If above 75% the max value, show, otherwise blank.
nx.draw_networkx_labels(G, pos,labels=labels,font_weight='bold',font_color='r')

f.savefig(TOPIC.title() + ' sociogram2.jpg')
plt.show()

nx.write_gexf(G,"trial.gexf")

# If user clicks on the node, show the name, sentiment, etc. show egodensity network
