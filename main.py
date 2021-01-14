
import sys
from stakeholderSNA_fns import drawEgoFromFile,drawCommFromFile,drawWholeNetworkFromFile,saveSummary,drawActivityOverTime
import matplotlib.pyplot as plt

# CONSTANTS
ARG_R_FILE = "-replyfile:"
ARG_EGO_USER = "-egouser:"
ARG_COLOR = "-color:"
ARG_TOPN = "-top:"
ARG_RECIP = "-reciprocal"
ARG_MODE = "-mode:"
RECIPROCAL_ON = 1
EGO = 1
INDIV_COMM = 2
WHOLE_NET = 3
CSV_SUMM = 4
OVER_TIME = 5
END = 6
COMMUNITY = 1
SENTIMENT = 2
ACTION_CALL = 3
NO_COLOR = 4

# DEFAULT VALUES
repliesFile = None
reciprocal = False
egoUser = None
color = None
topN = 100
block = False
colorOption = None

def askVisType():
	visType = input("\nWhat visualisation would you like to make?\n1) Egocentric (i.e. one user in the center)\n2) Individual communities (find all the clusters and draw each on a separate image)\n3) Whole network\n4) Create CSV summary of user centrality and communities\n5) Create line graph of network activity over time\n6) End the program\n")
	return int(visType)

def askEgoUser():
	egoUser = input("\nWhat is the username of the person you'd like to be in the center? (Check your .csv datafile for valid usernames)\n")
	return egoUser

def askColorParam():
	colorParam = input("\nWhat would you like the node colours to represent?\n1) Community allocations\n2) Sentiment (Green = Positive, Yellow = Neutral, Red = Negative, Grey = Unknown)\n3) Calls for action\n4) No color/ all gray\n")
	return int(colorParam)

def askReciprocal():
	reciprocalFlag = input('\nEvaluate communities based on reciprocal connections?\n1) Yes\n2) No\n')
	reciprocalFlag = int(reciprocalFlag)
	if reciprocalFlag == RECIPROCAL_ON:
		return True
	else:
		return False

############### MAIN #####################

if __name__ == "__main__":

	userParam = sys.argv[1:]
	if len(sys.argv) == 1:
		repliesFile = input("What is your data file name (containing scraped Twitter posts & replies)?\n")	# Only ask once

	for i in range(20):

		# RETRIEVE user parameters
		if len(sys.argv) == 1:
			visType = askVisType()
			if visType == EGO: egoUser = askEgoUser()
			if visType == EGO or visType == INDIV_COMM or visType == WHOLE_NET:	colorOption = askColorParam()
			if visType == INDIV_COMM or visType == CSV_SUMM or colorOption == COMMUNITY: reciprocal = askReciprocal()
		else:
			for param in userParam:
				# Data files
				if ARG_R_FILE in param: repliesFile = param[len(ARG_R_FILE):]

				# Mode parameters
				elif ARG_MODE in param: mode = param[len(ARG_MODE):]

				# Generic sociogram visualisation parameters
				elif ARG_COLOR in param: color = param[len(ARG_COLOR):]
				elif ARG_TOPN in param: topN = int(param[len(ARG_TOPN):])

				# Other specific parameters
				elif ARG_EGO_USER in param: egoUser = param[len(ARG_EGO_USER):]
				elif ARG_RECIP in param: reciprocal = True

			# Mode options
			if mode == "egocentric": visType = EGO
			elif mode == "individual": visType = INDIV_COMM
			elif mode == "whole": visType = WHOLE_NET
			elif mode == "summary": visType = CSV_SUMM
			elif mode == "overtime": visType = OVER_TIME

			# If drawing sociograms, color represents:
			if color == "community": colorOption = COMMUNITY
			elif color == "sentiment": colorOption = SENTIMENT
			elif color == "action":	colorOption = ACTION_CALL
			else: colorOption = NO_COLOR
			
			block = True	# Wait until user closes the visualisation window until advancing in code.

		# PROCESS parameters and EXECUTE request
		if visType == EGO:
			drawEgoFromFile(repliesFile,egoUser,colorRepresents=colorOption,reciprocal=reciprocal,saveAndClose=False,block=block)
		elif visType == INDIV_COMM:
			drawCommFromFile(repliesFile,topN,colorRepresents=colorOption,reciprocal=reciprocal,saveAndClose=False,block=block)
		elif visType == WHOLE_NET:
			drawWholeNetworkFromFile(repliesFile,topN,colorRepresents=colorOption,reciprocal=reciprocal,saveAndClose=False,block=block)
		elif visType == CSV_SUMM:
			saveSummary(repliesFile,reciprocal=reciprocal)
		elif visType == OVER_TIME:
			drawActivityOverTime(repliesFile,saveAndClose=False,block=block)
		elif visType == END:
			break

		print("\n*** TASK COMPLETED ***\n")

		if len(sys.argv) > 1: break	# If CLA were used, only execute once.

