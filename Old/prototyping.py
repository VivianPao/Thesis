
# GOAL: Save dictionary data to JSON file.
# Load dictionary from JSON file

import json

dictionary = {}

name = ["Linny57284055",
"NoBCA2",
"Rawsa7",
"NobcaA",
"PaulFletcherMP",
"flyWSA",
"ScottMorrisonMP",
"smh",
"araluenvalley",
"abcnews"]

# Writing dictionary
manualSentiment = {}
for i in range(len(name)):
	manualSentiment[name[i]] = 0	# Neutral sentiment to start with
with open("manualSentiment.json", "w") as f:
    json.dump(manualSentiment,f)


# Read dictionary from JSON
# with open('manualSentiment.json', 'r') as f:
#     manualSentiment = json.load(f)
# print(manualSentiment)