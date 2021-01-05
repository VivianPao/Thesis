
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
# print(len(followsDf))

numMembersList = []
densityList = []
posMemList = []
negMemList = []
actionCallNumList = []
actionCallList = []
numPostingList = []


totalNetworkDf = pd.DataFrame()

for X in range(42):

	# Get member list
	csv = pd.read_csv('comm'+str(X)+'.csv',index_col=0)	# Be careful with indexing. Name the column 'username'
	memberList = list(csv['degree'])
	additionalDf = pd.DataFrame({X:memberList})
	totalNetworkDf = pd.concat([totalNetworkDf, additionalDf], axis=1) 

	# Keep only the sentiment for members --> color
	subPostDf = postsDf[postsDf.username.isin(memberList)]	# Get the posts of all the users in the network if they exist in the post network
	posCount = sum(map(lambda x : x > 0, list(subPostDf['sentiment'])))
	negCount = sum(map(lambda x : x < 0, list(subPostDf['sentiment'])))

	subPostDf['color'] = subPostDf['tweet'].apply(calls2Action2Color)
	if any(subPostDf.color == 'r'):
		actionDf = subPostDf.loc[subPostDf.color == 'r']
		usersCallingAction = list(actionDf['username'])
		actionCallNum = len(usersCallingAction)
	else:
		usersCallingAction = []
		actionCallNum = 0

	numPosting = len(subPostDf)

	edgeDf = keepOnlyUsers(followsDf,memberList,strictFilterCol='followings')
	edgesDict = __mergeDictCol__(edgeDf['followings'])

	G = nx.Graph()
	G.add_edges_from(edgesDict)
	density = nx.density(G)

	numMembersList.append(len(memberList))
	posMemList.append(posCount)
	negMemList.append(negCount)
	densityList.append(density)
	actionCallNumList.append(actionCallNum)
	actionCallList.append(usersCallingAction)
	numPostingList.append(numPosting)

percentageNeg = [negMemList[i]/len(memberList) for i in range(len(negMemList))]

df = pd.DataFrame()
df['Number of Members'] = numMembersList
df['Density'] = densityList
df['Number of Positive Members'] = posMemList
df['Number of Negative Members'] = negMemList
df['Percentage of Negative Members'] = percentageNeg
df['Number of users calling for action'] = actionCallNumList
df['Users calling for action'] = actionCallList
df['Number of posting users'] = numPostingList
df.to_csv('summaryStats.csv')

totalNetworkDf.to_csv('Summary_All_Member_Lists.csv')




# # Identify which group the user is from
# findUser = 'faully33'
# for X in range(42):
# 	csv = pd.read_csv('comm'+str(X)+'.csv',index_col=0)	# Be careful with indexing. Name the column 'username'
# 	memberList = list(csv['degree'])
# 	if findUser in memberList:
# 		print(X)
# 		break




