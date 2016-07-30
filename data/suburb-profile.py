#+----------------------------------------------------------------------------+
#|           author: Bobby Koteski - last update: 30/7/2016                   |
#+----------------------------------------------------------------------------+ 

import csv

# dictionary to store csv data into program memory
local = {}

# read crime data
with open('crime.csv', 'r') as csvfile:
	reader = csv.reader(csvfile,delimiter=',')
	for row in reader:
		try:
			local[row[0]] = {'crime' : int(row[5])}
		except ValueError:
			pass

# read census data
with open('census.csv', 'r') as csvfile:
	reader = csv.reader(csvfile,delimiter=',')
	for row in reader:
		suburb = row[0][3:]
		if suburb in local:
			local[suburb]['medianAge'] = int(row[1])
			local[suburb]['medianMortgage'] = int(row[2])
			local[suburb]['medianSalary'] = int(row[3])
			local[suburb]['medianRent'] = float(row[4])
			local[suburb]['familySalary'] = int(row[5])
			local[suburb]['avergePersons'] = float(row[7])

print local['3000']