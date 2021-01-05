
import pandas as pd
from sociogramFunctions import *

N = 10
X = 0

# def sentiment2Color(score):
# 	if score < 0:
# 		return 'r'
# 	elif score > 0:
# 		return 'g'
# 	else:
# 		return 'y'

# def analyseCalls2Action(text):
# 	wordBank = ["petition","protest","letter","strike"]
# 	score = 0
# 	for word in wordBank:
# 		score += text.count(word)
# 	return score

# def calls2Action2Color(text):
# 	score = analyseCalls2Action(text)
# 	if score > 0:
# 		return 'r'
# 	else:
# 		return 'gray'


def analyseSentiment(text):
	wordBank = ["petition","protest","letter","strike"]
	score = 0
	for word in wordBank:
		score += text.count(word)
	return score

def setSentimentColor(text):
	score = analyseSentiment(text)
	if score > 0:
		return 'r'
	else:
		return 'gray'


postsDf = pd.read_csv('allPosts.csv')
followsDf = pd.read_json('allFollowings.json')
followsDf['followings'] = followsDf['followings'].apply(turn2LiteralKeys)

# over50 = [0,1,2,3,4,6,7,8,9,12,13,14,15]
over50 = [15]

showSentiment = True#False
showCalls2Action = False#True


# Plot every community, highlight the calls to action
for X in over50:#range(42):

	# Get member list
	csv = pd.read_csv('comm'+str(X)+'.csv',index_col=0)	# Be careful with indexing. Name the column 'username'
	memberList = list(csv['degree'])

	# Keep only the sentiment for members --> color
	if showSentiment == True:
		sentimentDf = postsDf[postsDf.username.isin(memberList)]
		sentimentDf['color'] = sentimentDf['sentiment'].apply(sentiment2Color)
		colorDict = dict(zip(list(sentimentDf['username']),list(sentimentDf['color'])))
	elif showCalls2Action == True:
		# Make users that have made calls to action red
		colorDf = postsDf[postsDf.username.isin(memberList)]
		colorDf['color'] = postsDf['tweet'].apply(calls2Action2Color)

		if any(colorDf.color == 'r'):
			actionDf = colorDf.loc[colorDf.color == 'r']
			usersCallingAction = list(actionDf['username'])
			labels = usersCallingAction

		colorDict = dict(zip(list(colorDf['username']),list(colorDf['color'])))

	# colorDict = dict(zip(memberList,['mediumorchid']*len(memberList)))
	colorDict['peterjameswills'] = 'gray'

	# Get following edges 
	edgeDf = keepOnlyUsers(followsDf,memberList,strictFilterCol='followings')

	# Get overall centrality for node sizing
	cDf = calcOverallCentrality(edgeDf,'followings')
	cDf = cDf.sort_values(by='overall',ascending=False)
	overallCenDict = dict(zip(list(cDf['username']),list(cDf['overall'])))

	# Get top N labels
	labels = list(cDf['username'])
	labels = labels[:N]
	labels = usersCallingAction
	labels.remove('peterjameswills')

	drawGraph(edgeDf,'followings',labelList=labels,title='calls2action_comm'+str(X)+'.csv',colorDict=colorDict,minSize=20,sizeScale=100,widthScale=1,edgeAlpha=0.1,block=False,saveAndClose=True)

