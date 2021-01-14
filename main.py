
from stakeholderSNA_fns import drawEgoFromFile,drawCommFromFile,drawWholeNetworkFromFile,saveSummary,drawActivityOverTime
import matplotlib.pyplot as plt

labelTopN = 100
RECIPROCAL_ON = 1
EGO = 1
INDIV_COMM = 2
WHOLE_NET = 3
CSV_SUMM = 4
OVER_TIME = 5
END = 6

REPLIES = 0
FOLLOWS = 1
INVALID = -1

# Whole network over time
MONTHLY_CHAR = 7
FULL_DATE_CHAR = 19

COMMUNITY = 1
SENTIMENT = 2
ACTION_CALL = 3
NO_COLOR = 4

def askVisType():
	visType = input("\nWhat visualisation would you like to make?\n1) Egocentric (i.e. one user in the center)\n2) Individual communities (find all the clusters and draw each on a separate image)\n3) Whole network\n4) Create CSV summary of user centrality and communities\n5) Create line graph of network activity over time\n6) End the program\n")
	return int(visType)

def askEgoUser():
	egoUser = input("\nWhat is the username of the person you'd like to be in the center? (Check your .csv datafile for valid usernames)\n")
	return egoUser

def askColorParam():
	colorParam = input("\nWhat would you like the node colours to represent?\n1) Community allocations\n2) Sentiment (Green = Positive, Yellow = Neutral, Red = Negative, Grey = Unknown)\n3) Calls for action\n4) No color/ all gray\n")
	return int(colorParam)

# def askCommSource():
# 	source = input("\nWhich community data would you like to visualise on the graph?\n1) Communities based on replies clustering\n2) Communities based on follower clustering\n")
# 	return int(source)

# def checkSourcePossible(data2Show,repliesStatus,followsStatus):
# 	if data2Show == REPLIES and repliesStatus is not None:
# 		return True
# 	elif data2Show == FOLLOWS and followsStatus is not None:
# 		return True
# 	else:
# 		return False

def askReciprocal():
	reciprocalFlag = input('\nEvaluate communities based on reciprocal connections?\n1) Yes\n2) No\n')
	reciprocalFlag = int(reciprocalFlag)
	if reciprocalFlag == RECIPROCAL_ON:
		return True
	else:
		return False

############### MAIN #####################

if __name__ == "__main__":

	"""
	newDataFlag = input("Do you want to scrape Twitter for new data or visualise data you've already scraped?\n1) Scrape new data\n2) Visualise existing data\n")
	newDataFlag = int(newDataFlag)

	if newDataFlag == 1:

		# Get search parameters
		topic = input("\nWhat topic would you like to search on Twitter?\n")
		dateFrom = input("\nWhat date would you like to scrape FROM? (YYYY-MM-DD)\n")
		dateTo = input("\nWhat date would you like to scrape TO? (YYYY-MM-DD)\n")
		repliesFile = input("\nWhat would you like to save the data file as? (include '.csv' at end, use letters, numbers and underscores only.)\n")

		# Scrape data and save
		print("\nNow scraping data...")
		data = scrapeTopic(topic,dates=[dateFrom,dateTo])
		data.to_csv(repliesFile)

	elif newDataFlag == 2:
		repliesFile = input("\nWhat is the data file called? (include '.csv')\n")
	"""

	repliesFile = None#"test.csv"
	followsFile = None

	primaryFile = "X"
	secondaryFile = "Y"
	# Load the files then put the DF into the functions!

	for i in range(100):
		reciprocal = None
		colorOption = None
		visType = askVisType()

		# RETRIEVE parameters from user input
		repliesFile = input("What is your data file name (containing scraped Twitter posts & replies)?")
		if visType == EGO: egoUser = askEgoUser()
		if visType == EGO or visType == INDIV_COMM or visType == WHOLE_NET:	colorOption = askColorParam()
		if visType == INDIV_COMM or visType == CSV_SUMM or colorOption == COMMUNITY: reciprocal = askReciprocal()

		# PROCESS parameters and EXECUTE request
		if visType == EGO:
			drawEgoFromFile(repliesFile,egoUser,colorRepresents=colorOption,reciprocal=reciprocal,saveAndClose=False)
		elif visType == INDIV_COMM:
			drawCommFromFile(repliesFile,labelTopN,colorRepresents=colorOption,reciprocal=reciprocal,saveAndClose=False)
		elif visType == WHOLE_NET:
			drawWholeNetworkFromFile(repliesFile,labelTopN,colorRepresents=colorOption,reciprocal=reciprocal,saveAndClose=False)
		elif visType == CSV_SUMM:
			saveSummary(repliesFile,reciprocal=reciprocal)
		elif visType == OVER_TIME:
			drawActivityOverTime(repliesFile,saveAndClose=False)
		elif visType == END:
			break
		print("\n*** TASK COMPLETED ***\n")

	# for i in range(100):
	# 	reciprocal = None
	# 	visType = askVisType()

	# 	if visType == EGO:
	# 		egoUser = askEgoUser()
	# 		colorOption = askColorParam()
	# 		if colorOption == COMMUNITY: reciprocal = askReciprocal()
	# 		drawEgoFromFile(repliesFile,egoUser,colorRepresents=colorOption,reciprocal=reciprocal,saveAndClose=False)

	# 	elif visType == INDIV_COMM:
	# 		colorOption = askColorParam()
	# 		reciprocal = askReciprocal()
	# 		drawCommFromFile(repliesFile,labelTopN,colorRepresents=colorOption,reciprocal=reciprocal,saveAndClose=False)

	# 	elif visType == WHOLE_NET:
	# 		colorOption = askColorParam()
	# 		if colorOption == COMMUNITY:
	# 			reciprocal = askReciprocal()
	# 		drawWholeNetworkFromFile(repliesFile,labelTopN,colorRepresents=colorOption,reciprocal=reciprocal,saveAndClose=False)

	# 	elif visType == CSV_SUMM:
	# 		reciprocal = askReciprocal()
	# 		saveSummary(repliesFile,reciprocal=reciprocal)

	# 	elif visType == OVER_TIME:
	# 		drawActivityOverTime(repliesFile,saveAndClose=False)

	# 	elif visType == END:
	# 		break

		# print("\n*** TASK COMPLETED ***\n")
	# """
