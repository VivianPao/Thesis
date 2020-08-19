
import twint

# If the user has been seen before, increment their count. If not, add them into the dictionary and set count to 1.
def __addToDict__(dictName,keyValue):
	if keyValue not in dictName:
		dictName[keyValue] = 1
	else:
		dictName[keyValue] += 1

# Based on the posts of a topic, find all the users that have mentioned a particular person on a topic (or no topic)
def findMentioning(topic,tweetLimit):
	FROM = 0
	TO = 1
	
	c = twint.Config()
	c.Limit = tweetLimit
	c.Pandas = True
	c.Search = topic
	c.Format = "{username} | {mentions}"
	twint.run.Search(c)

	collectedData = twint.storage.panda.Tweets_df	# Dataframe of series!
	mentions = collectedData.loc[:,('reply_to')]

	mentionsDict = {}	# Key: edge tuple. Value: weight
	usersDict = {}	# Key: username. Value: How many times appeared
	for row in range(len(mentions)):
		for nthMention in range(TO,len(mentions[row])):	# For each mentioned user, create a new link to the poster
			source = mentions[row][FROM]['username']
			target = mentions[row][nthMention]['username']
			linkTuple = (source,target)

			__addToDict__(mentionsDict,linkTuple)
			__addToDict__(usersDict,source)
			__addToDict__(usersDict,target)

	return (usersDict,mentionsDict)


def getTweetsFrom(user,topic,tweetLimit):
	# Warning, Twint is VERY slow when getting tweets from specific users
	c = twint.Config()
	c.Limit = tweetLimit
	c.Pandas = True
	c.Username = user
	c.Format = "{username} | {tweet}"
	c.Search = topic
	twint.run.Search(c)

	collectedData = twint.storage.panda.Tweets_df	# Dataframe of series!
	if collectedData.empty == False:
		tweets = collectedData['tweet'].astype(str).tolist()
	else:	# If there wasn't any data, return an empty list
		tweets  = []
		
	return tweets

