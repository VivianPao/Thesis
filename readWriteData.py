
import pandas as pd
import ast

def readDataCSV(nameFile):	# Dicts by default in string format. Rewrite the column with real dicts.
	try:
		collectedData = pd.read_csv(nameFile)
	except:
		print('File ' + nameFile + ' does not exist')
		collectedData = pd.DataFrame()
		return collectedData
		
	weightedLinks = collectedData['reply_to'].tolist()	# List of dicts
	columnIndex = collectedData.columns.get_loc('reply_to')
	for i in range(len(weightedLinks)):		
		collectedData.iloc[i,columnIndex] = [ast.literal_eval(weightedLinks[i])]
	return collectedData