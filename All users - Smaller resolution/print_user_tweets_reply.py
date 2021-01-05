
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
postingUsersList = list(postsDf['username'])
followsDf = pd.read_json('allFollowings.json')
followsDf['followings'] = followsDf['followings'].apply(turn2LiteralKeys)

indeg = listTopCentralityUsers(postsDf,'reply_to',centralityType='indegree')
outdeg = listTopCentralityUsers(postsDf,'reply_to',centralityType='outdegree')

top10TweetSummary = pd.DataFrame()

for topList in [indeg,outdeg]:

	top10List = topList

	# We will have less posting users than following network users because not everyone posts.
	for user in top10List:
		if user in postingUsersList:
			tweet = postsDf.loc[postsDf['username'] == user]['tweet']

			if tweet is not None:
				subDf = pd.DataFrame({'community':[X],'username':user,'tweet':tweet})
		else:
			subDf = pd.DataFrame({'community':[X],'username':user,'tweet':'N/A'})

		top10TweetSummary = pd.concat([top10TweetSummary,subDf],axis=0)

	# subDf = postsDf[postsDf.username.isin(top10List)][['username','tweet','sentiment']]

	# print(len(memberList))
	# print(len(list(subDf['username'])))
# 	subDf['Community'] = [i]*len(memberList)
# 	top10TweetSummary = pd.concat([top10TweetSummary,subDf],axis=0)

top10TweetSummary.to_csv('All_reply_top'+str(N)+'users_tweets.csv')


print('in degree')
for i in range(10):
	print(indeg[i])

print('out degree')
for i in range(10):
	print(outdeg[i])