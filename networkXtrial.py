
import matplotlib.pyplot as plt
import networkx as nx

G = nx.cubical_graph()
pos = nx.spring_layout(G) # positions for all nodes

# Consider ways to organise data and draw the network in most efficient way.
# Possibly draw nodes in groups, e.g. all node that are strong poitive, or nodes that are most influential (large node size)
# Same with edges...

nodes = ['Tohru','Kyo','Yuki']

# Node list... maybe each node should be a number. Make this number a key in a dictionary?
# Indices are important... everything msut correspond here!

# nodes
nx.draw_networkx_nodes(G, pos,
                       nodelist=[0,1,2],
                       node_color=['g','r','b'],
                       node_size=[500,400,300])

# edges. Any number of tuples in this edge list
nx.draw_networkx_edges(G, pos,
                       edgelist=[(0,1), (0,2), (1,2)],
                       width=[18,2,2], alpha=0.5, edge_color='r')

labels = {}
labels[0] = nodes[0]
labels[1] = nodes[1]
labels[2] = ''			# You can leave the label blank for some... How to selectively show node names.
nx.draw_networkx_labels(G, pos, labels, font_size=16)

plt.axis('off')
plt.show()