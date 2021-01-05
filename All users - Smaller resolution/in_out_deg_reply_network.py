
# Unidirectional egocentric networks: replies and follows

import pandas as pd
from sociogramFunctions import *

def __mergeDictCol__(dfColumn):
	dictList = list(dfColumn)
	dictList = [d for d in dictList if d != {}]
	edgesDict = dict(ChainMap(*dictList))	# Merge all dictionaries
	return edgesDict

def turn2LiteralKeysReply(dictionary):
	return eval(dictionary)

postsDf = pd.read_csv('allPosts.csv')
postsDf['reply_to'] = postsDf['reply_to'].apply(turn2LiteralKeysReply)
followsDf = pd.read_json('allFollowings.json')
followsDf['followings'] = followsDf['followings'].apply(turn2LiteralKeys)

indeg = listTopCentralityUsers(postsDf,'reply_to',centralityType='indegree')
outdeg = listTopCentralityUsers(postsDf,'reply_to',centralityType='outdegree')

print('in degree')
for i in range(10):
	print(indeg[i])

print('out degree')
for i in range(10):
	print(outdeg[i])


# lynlinking
# BridgetOFlynn
# brucerossbrc
# MSMWatchdog2013
# davidbewart
# daveyk317
# YaThinkN
# randlight
# edwardatport
# MarekRivers
