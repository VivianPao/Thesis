
import sys
from scraping import scrapeTopic

# Default values
topic = None
dateFrom = None
dateTo = None
repliesFile = "untitled.csv"

ARG_TOPIC = "-topic:"
ARG_FROM = "-from:"
ARG_TO = "-to:"
ARG_OUTPUT = "-output:"

if __name__ == "__main__":

	# If command line arguments not detected, show guided prompts
	if len(sys.argv) == 1:
		# Get search parameters
		topic = input("\nWhat topic would you like to search on Twitter?\n")
		dateFrom = input("\nWhat date would you like to scrape FROM? (YYYY-MM-DD)\n")
		dateTo = input("\nWhat date would you like to scrape TO? (YYYY-MM-DD)\n")
		repliesFile = input("\nWhat would you like to save the data file as? (include '.csv' at end, use letters, numbers and underscores only.)\n")
	else:
		userParam = sys.argv[1:]
		for param in userParam:
			if ARG_TOPIC in param:
				topic = param[len(ARG_TOPIC):]
			elif ARG_FROM in param:
				dateFrom = param[len(ARG_FROM):]
			elif ARG_TO in param:
				dateTo = param[len(ARG_TO):]
			elif ARG_OUTPUT in param:
				repliesFile = param[len(ARG_OUTPUT):]

	# Scrape data and save
	print("\nNow scraping data...\n")
	data = scrapeTopic(topic,dates=[dateFrom,dateTo])
	data.to_csv(repliesFile)
	print("\nDone.\n")

# python main_scrape.py -topic:"badgerys creek airport" -from:2020-02-01 -to:2020-06-01 -output:other.csv