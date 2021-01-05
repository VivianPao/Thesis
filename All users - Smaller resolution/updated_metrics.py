
import pandas as pd
from sociogramFunctions import *

N = 10
X = 0

def __mergeDictCol__(dfColumn):
	dictList = list(dfColumn)
	dictList = [d for d in dictList if d != {}]
	edgesDict = dict(ChainMap(*dictList))	# Merge all dictionaries
	return edgesDict

postsDf = pd.read_csv('allPosts.csv')
followsDf = pd.read_json('allFollowings.json')
followsDf['followings'] = followsDf['followings'].apply(turn2LiteralKeys)

numMembersList = []
densityList = []
numPostingList = []
topUsers = []

over50 = [0,1,2,3,4,6,7,8,9,12,13,14,15]

for X in over50:

	print(X)

	# Get member list
	csv = pd.read_csv('comm'+str(X)+'.csv',index_col=0)	# Be careful with indexing. Name the column 'username'
	memberList = list(csv['degree'])
	additionalDf = pd.DataFrame({X:memberList})

	subPostDf = postsDf[postsDf.username.isin(memberList)]	# Get the posts of all the users in the network if they 
	numPosting = len(subPostDf)

	followsDf_oCen = pd.read_csv('oCentrality_comm'+str(X)+'.csv')
	listTopUsers = list(followsDf_oCen.iloc[0:10]['username'])

	edgeDf = keepOnlyUsers(followsDf,memberList,strictFilterCol='followings')
	edgesDict = __mergeDictCol__(edgeDf['followings'])

	G = nx.Graph()
	G.add_edges_from(edgesDict)
	density = nx.density(G)

	numMembersList.append(len(memberList))
	densityList.append(density)
	numPostingList.append(numPosting)
	topUsers.append(listTopUsers)

df = pd.DataFrame()
df['Community'] = over50
df['Number of Members'] = numMembersList
df['Community Density'] = densityList
df['Number of posting users'] = numPostingList
df['Percentage of posting users'] = df['Number of posting users']/df['Number of Members']
df['Top 10 users'] = topUsers
df.to_csv('UPDATED_summaryStats.csv')



