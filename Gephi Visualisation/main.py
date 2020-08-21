
import twint
import pandas as pd

TWEET_LIM = 500

# Based on the posts of a topic, find all the users that have mentioned a particular person on a topic (or no topic)
def gephi_FindMentioning(topic,tweetLimit):
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

	source = []
	target = []
	for row in range(len(mentions)):
		for nthMention in range(TO,len(mentions[row])):	# For each mentioned user, create a new link to the poster
			source.append(mentions[row][FROM]['username'])
			target.append(mentions[row][nthMention]['username'])

	finalData = pd.DataFrame({'Source': source,'Target': target})
	finalData['Link'] = [1] * len(finalData.index)
	finalData['Sentiment'] = [1] * len(finalData.index)

	return finalData

# def getTweetsFrom(user,topic,tweetLimit):
# 	# Warning, Twint is VERY slow when getting tweets from specific users
# 	c = twint.Config()
# 	c.Limit = tweetLimit
# 	c.Pandas = True
# 	c.Username = user
# 	c.Format = "{username} | {tweet}"
# 	c.Search = topic
# 	twint.run.Search(c)

# 	collectedData = twint.storage.panda.Tweets_df	# Dataframe of series!
# 	if collectedData.empty == False:
# 		tweets = collectedData['tweet'].astype(str).tolist()
# 	else:
# 		tweets  = []
		
# 	return tweets

if __name__ == "__main__":
	topic = "Fruits Basket"
	finalTable = gephi_FindMentioning(topic,TWEET_LIM)
	finalTable.to_csv(topic + ".csv",index = False)
	print(finalTable)



