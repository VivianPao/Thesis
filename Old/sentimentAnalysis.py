
# Sentiment Analysis Tool

# Considerations:
# Set up: Weighted sentiment for words. Perhaps use dictionary
# Preprocessing: Spelling, punctuation, capitalisation variations
# Processing: Change check to allow you to check how many times a word comes up (may be more than once)
# Combination of words, e.g. 'not happy, unhappy', characters: "angry!"

# ********************** FUNCTIONS ************************

# Find better way to calc sentiment
# Need to import word banks

class sentimentAnalyser:

	def __init__(self):
		self.posBank = ["happy","excited","glad"]
		self.negBank = ["sad","angry","upset"]

	# Calculate how many of the words in the wordPool are in the sentence
	def __calcPos__(self,text):
		score = 0
		for word in self.posBank:
			score += text.count(word)
		return score

	def __calcNeg__(self,text):
		score = 0
		for word in self.negBank:
			score += text.count(word)
		return score		

	# Add the positive and negative scores together (with the negative scores being negative numbers)
	# Positive/ negative sign of the sentiment score reflects sentiment
	def calcTextSentiment(self,text):
		posScore = self.__calcPos__(text)
		negScore = self.__calcNeg__(text)
		total = posScore - negScore
		return total

	def calcUserSentiment(self,listOfStrings):
		sentiment = 0
		for string in listOfStrings:
			sentiment += self.calcTextSentiment(string)
		return sentiment

# ********************** MAIN ************************

sentence = "I'm not happy!"	# Tricky case for analysis...

mySA = sentimentAnalyser()
sentiment = mySA.calcUserSentiment([sentence,sentence,sentence])
print("Sentiment score:",sentiment)



