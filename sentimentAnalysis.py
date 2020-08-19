
from textblob import TextBlob

def calcTextSentiment(text):
	text = TextBlob(text)
	analysis = text.sentiment.polarity
	return analysis

def calcUserSentiment(listOfStrings):
	sentiment = 0	# Initial sentiment of 0
	if len(listOfStrings) == 0:
		return sentiment
	else:
		# Calculate individual string sentiment and then get the average
		for string in listOfStrings:
			sentiment += calcTextSentiment(string)
		sentiment /= len(listOfStrings)
		return sentiment

