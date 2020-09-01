
import pandas as pd

def __addToDict__(dictName,keyValue):
	if keyValue not in dictName:
		dictName[keyValue] = 1
	else:
		dictName[keyValue] += 1

def createLinksDict(listOfDicts):
	linkTo = dict()
	for i in range(1,len(listOfDicts)):
		d = listOfDicts[i]
		mentionedUser = d['username']
		__addToDict__(linkTo,mentionedUser)
	return linkTo


dictA = dict({"id": 1, "username": "random Heh"})
d = {'username': ["vivian", "derek"], 'tweet': ["sample tweet A", "sample tweet B"], 'reply_to': [[dictA,dictA],[dictA,dictA]]}

df = pd.DataFrame(d)
replyDf = df['reply_to']

df.at[0,'reply_to'] = 99
print(df)

# grouped = tweetDf.groupby('username')
# tweetDf = grouped.apply(list)

# grouped = replyDf.groupby('username')
# replyDf = grouped.aggregate(someFunc)


# for row in df.iterrows():
	





# d = dict({"A":[1,2,3,1],"B":[4,5,6,1],"C":[7,8,9,1]}) 
# df = pd.DataFrame(d)
# print(df)
# grouped = df.groupby('A')	# combines duplicates, make a tuple of all other columns
# print(grouped)
# df = grouped.aggregate(lambda x: list(x))
# print(df)

