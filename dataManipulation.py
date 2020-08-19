
import numpy as np

# Given an array and a value, delete the first instance of the value from the array
def __deleteElement__(givenArray,givenVal):
	returnArray = []
	for val in givenArray:
		if val is not givenVal:
			returnArray.append(val)
	return returnArray

# Given an array, find the indices of the top n values. Highest priority first.
def findTopNindices(givenArray,n):
	# If n is larger than the length of the array, set 'n' to the length
	if n > len(givenArray):
		n = len(givenArray)

	# Find indices that give top n values
	topNindices = np.argpartition(givenArray, -n)[-n:]

	# Reorganise indices in descending order
	unordered = list(topNindices)	# Need to make sure you cast as list(). Else it doesn't work
	ordered = []
	for i in range(n):	# Run n times
		maxIndex = unordered[0]
		maxVal = givenArray[maxIndex]
		for index in unordered:
			if givenArray[index] > maxVal:	# If element greater than max stored
				maxVal = givenArray[index]	# Set max to this. Eventually find max in the array.
				maxIndex = index

		ordered.append(maxIndex)
		unordered = __deleteElement__(unordered,maxIndex)

	return ordered
