
# Sentiment Analysis Tool

# Sentiment between -1 and 1 polarity values.

# ********************** FUNCTIONS ************************

# Find better way to calc sentiment
# Import word banks

from textblob import TextBlob

# Add the positive and negative scores together (with the negative scores being negative numbers)
# Positive/ negative sign of the sentiment score reflects sentiment
def calcTextSentiment(text):
	text = TextBlob(text)
	analysis = text.sentiment.polarity
	return analysis

def calcUserSentiment(listOfStrings):
	sentiment = 0
	for string in listOfStrings:
		sentiment += calcTextSentiment(string)
	sentiment /= len(listOfStrings)
	return sentiment

# ********************** MAIN ************************

sentence = "How could you do this to us? Unbelievable"	# Tricky case for analysis...

sentiment = calcUserSentiment([sentence,sentence,sentence])
print("Sentiment score:",sentiment)



