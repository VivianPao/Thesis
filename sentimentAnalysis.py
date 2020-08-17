
# Sentiment Analysis Tool

# Considerations:
# Set up: Weighted sentiment for words. Perhaps use dictionary
# Preprocessing: Spelling, punctuation, capitalisation variations
# Processing: Change check to allow you to check how many times a word comes up (may be more than once)
# Combination of words, e.g. 'not happy, unhappy', characters: "angry!"

# ********************** FUNCTIONS ************************

# Check if a small string is in a big string
def __checkSubstring__(text,substring):
	if substring in text:
		return 1
	else:
		return 0

# Calculate how many of the words in the wordPool are in the sentence
def calcScore(text,wordBank):
	score = 0
	for word in wordBank:
		score += __checkSubstring__(text,word)
	return score

# Add the positive and negative scores together (with the negative scores being negative numbers)
# Positive/ negative sign of the sentiment score reflects sentiment
def calcSentiment(posScore,negScore):
	total = posScore - negScore
	return total

# ********************** MAIN ************************

sentence = "I'm not happy!"

posPool = ["happy","excited","glad"]
negPool = ["sad","angry","upset"]

posScore = calcScore(sentence,posPool)
negScore = calcScore(sentence,negPool)
sentiment = calcSentiment(posScore,negScore)

print("Sentiment score:",sentiment)