
import pandas as pd
from sociogramFunctions import *

N = 10
X = 0

postsDf = pd.read_csv('allPosts.csv')
followsDf = pd.read_json('allFollowings.json')
followsDf['followings'] = followsDf['followings'].apply(turn2LiteralKeys)

over50 = [0,1,2,3,4,6,7,8,9,12,13,14,15]

# Plot every community, highlight the calls to action
for X in over50:

	csv = pd.read_csv('comm'+str(X)+'.csv',index_col=0)	# Be careful with indexing. Name the column 'username'
	memberList = list(csv['degree'])

	# Get following edges 
	edgeDf = keepOnlyUsers(followsDf,memberList,strictFilterCol='followings')

	# Get overall centrality for node sizing
	cDf = calcOverallCentrality(edgeDf,'followings')
	cDf_sorted = cDf.sort_values(by='overall',ascending=False)
	cDf_sorted.to_csv('Check_'+str(X)+'.csv')
	