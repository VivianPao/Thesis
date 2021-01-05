
from stakeholderSNA_fns import *

labelTopN = 100

topic = "something"
filename = "test.csv"
dateFrom = "2020-01-01"
dateTo = "2020-05-02"
egoUser = "Greens"

############### MAIN #####################

if __name__ == "__main__":

	newDataFlag = input("Do you want to scrape Twitter for new data or visualise data you've already scraped?\n1) Scrape new data\n2) Visualise existing data\n")

	if newDataFlag == "1":

		# Get search parameters
		topic = input("\nWhat topic would you like to search on Twitter?\n")
		dateFrom = input("\nWhat date would you like to scrape FROM? (YYYY-MM-DD)\n")
		dateTo = input("\nWhat date would you like to scrape TO? (YYYY-MM-DD)\n")
		filename = input("\nWhat would you like to save the data file as? (include '.csv' at end, use letters, numbers and underscores only.)\n")

		# Scrape data and save
		print("\nNow scraping data...")
		data = scrapeTopic(topic,dates=[dateFrom,dateTo])
		data.to_csv(filename)

	elif newDataFlag == "2":
		filename = input("\nWhat is the data file called? (include '.csv')\n")

	# Visualise
	for i in range(100):

		visType = input("\nWhat visualisation would you like to make?\n1) Egocentric (i.e. one user in the center)\n2) Individual communities (find all the clusters and draw each on a separate image)\n3) Whole network\n4) End the program\n")

		if visType == "1":
			egoUser = input("\nWhat is the username of the person you'd like to be in the center? (Check your .csv datafile for valid usernames)\n")
			drawEgoFromFile(filename,egoUser)
		elif visType == "2":
			drawCommFromFile(filename,labelTopN)
		elif visType == "3":
			drawWholeNetworkFromFile(filename,labelTopN)
		elif visType == "4":
			break 