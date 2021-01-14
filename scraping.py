
import twint
import pandas as pd

# TWITTER SCRAPING FUNCTIONS

# If the user has been seen before, increment their count. If not, add them into the dictionary and set count to 1.
def addToDict(dictName,keyValue):
	if keyValue not in dictName:
		dictName[keyValue] = 1
	else:
		dictName[keyValue] += 1


# Return dataframe with edge + weight dictionary
def organiseData(df):

	if df.empty:
		return df

	df = df[['date','username','tweet','reply_to']]	# concat string tweets and list of dicts
	df = df.groupby('username',as_index=False).aggregate(sum)	# Group by username (merge duplicates)

	# df.groupby('username',as_index=False).agg('\'.join)
	# print(df)

	# For each user/ row, rewrite the dictionary. key: mentioned users, val: weight
	# Use the apply() pandas function to create a new entry for the dictionary!
	for row in range(len(df)):
		username = df.iloc[row][0]
		listOfDicts = df.iloc[row]['reply_to']

		linkTo = {}	# Create dict, keys as tuples of user -> mentioned user: weight
		for aDict in listOfDicts:
			mentionedUser = aDict['screen_name']
			if mentionedUser != username: # As long as the user isn't replying to themselves, add them to the dictionary
				addToDict(linkTo,(username,mentionedUser))
		df.loc[df.username == username,'reply_to'] = [linkTo]

	return df

# Need to process/ reoganise the followings
def organiseFollows(df):
	return 0

# Based on the posts of a topic, find all the users that have mentioned a particular person on a topic (or no topic)
def scrapeTopic(topic,tweetLimit=None,dates=None):
# Dates in form ['YYYY-MM-DD','YYYY-MM-DD']
	c = twint.Config()

	if tweetLimit != None:
		c.Limit = tweetLimit
	
	c.Search = topic
	# c.Store_csv = True
	# The following features/ customisations do not work with the latest Twint version
	c.Pandas = True
	# c.Format = "{date}: {username} -> {mentions}" 
	if dates != None:
		[sinceDate,untilDate] = dates
		c.Since = sinceDate
		c.Until = untilDate

	twint.run.Search(c)

	df = organiseData(twint.storage.panda.Tweets_df)

	return df	# Dataframe of series!


def findFollowing(username,limitNum=10000):
	c = twint.Config()
	# c.Limit = limitNum
	c.Pandas = True
	c.Username = username
	twint.run.Following(c)

	collectedData = twint.storage.panda.Follow_df	# Dataframe of dataframes!
	targetData = collectedData.loc[:,('following')][username]	# Gives an array
	sourceData = [username] * len(targetData)
	finalData = pd.DataFrame({'A': sourceData,'B': targetData})
	# print(finalData)
	return finalData

def scrapeFollowings(userList):
	followerDf = pd.DataFrame()
	for user in userList:
		print('Searching: ',user)
		for attempt in range(10):
			try:
				data = findFollowing(user,None)
			except:
				print('Error for',user)
				continue
			followerDf = pd.concat([followerDf,data])
			followerDf.to_csv('followerData'+userList[len(userList)-1]+'.csv')
			break

	return followerDf
