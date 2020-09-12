
# These functions take in a start and end date (YYYY-MM) and create a list of date pairs to use for Twint searching

DAYS_IN_MONTH = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

def checkLeapYear(year):
	if year%4 == 0:
		if year%100 == 0:
			if year%400 == 0:
				return 1
			else:
				return 0
		else:
			return 1
	else:
		return 0

def getEndDay(year,month):
	if month == 2 and checkLeapYear(year) == 1:
		return 29
	else:
		return DAYS_IN_MONTH[month]

def getDateNumbers(startString,endString):
	startYear = int(startString[0:4])
	startMonth = int(startString[5:7])
	endYear = int(endString[0:4])
	endMonth = int(endString[5:7])
	return [startYear,startMonth,endYear,endMonth]

def getMonthlyDates(startDate,endDate):
	[startYear,startMonth,endYear,endMonth] = getDateNumbers(startDate,endDate)

	listDatePairs = []
	for y in range(startYear,endYear+1):
		if y != endYear:
			tempEndMonth = 12
		else:
			tempEndMonth = endMonth
			
		for m in range(startMonth,tempEndMonth+1):
			startMonthString =  str(y) + '-' + str(m).zfill(2) + '-' + '01'	# zfill(2) adds 0
			endMonthString = str(y) + '-' + str(m).zfill(2) + '-' + str((getEndDay(y,m))).zfill(2)
			startMonth = 1

			datePair = [startMonthString,endMonthString]
			listDatePairs.append(datePair)	# List of list of dates

	return listDatePairs

def getYearlyDates(startDate,endDate):
	[startYear,startMonth,endYear,endMonth] = getDateNumbers(startDate,endDate)

	listDatePairs = []
	for y in range(startYear,endYear+1):
		startYearString = str(y) + '-01-01'
		endYearString = str(y) + '-12-31'
		datePair = [startYearString,endYearString]
		listDatePairs.append(datePair)	# List of list of dates

	return listDatePairs

# import datetime
# s = '04/21/2013'
# date = datetime.datetime.strptime(s, '%m-%d-%Y')
# newDate = date + datetime.timedelta(days=1)
# print(d.strftime('%m-%d-%Y'))
# 04/22/2013

if __name__ == "__main__":
	start = '2015-05'
	end = '2016-07'

	a = getMonthlyDates(start,end)
	print(a)
