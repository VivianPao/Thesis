
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

top10TweetSummary = pd.DataFrame()

over50 = [0,1,2,3,4,6,7,8,9,12,13,14,15]
for i in range(len(over50)):
	X = over50[i]
	csv = pd.read_csv('oCentrality_comm'+str(X)+'.csv',index_col=0)	# Be careful with indexing. Name the column 'username'
	memberList = list(csv['username'])
	top10List = memberList[:N]

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

top10TweetSummary.to_csv('All_comm_top'+str(N)+'users_tweets.csv')
