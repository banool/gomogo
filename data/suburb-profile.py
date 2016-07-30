#+----------------------------------------------------------------------------+
#|           author: Bobby Koteski - last update: 30/7/2016                   |
#+----------------------------------------------------------------------------+ 

import csv

# dictionary to store csv data into program memory
local = {}

# load suburb names into local memory
with open('suburbnames.csv','r') as csvfile:
	reader = csv.reader(csvfile,delimiter=',')
	for row in reader:
		local[row[2]] = {'name' : row[1]}

# read crime data
with open('crime.csv', 'r') as csvfile:
	reader = csv.reader(csvfile,delimiter=',')
	for row in reader:
		suburb = row[0]
		if suburb in local:
			local[suburb]['crime'] = int(row[5])

# read census data
with open('census.csv', 'r') as csvfile:
	reader = csv.reader(csvfile,delimiter=',')
	for row in reader:
		# parse suburb, format:POA3xxx
		suburb = row[0][3:]
		if suburb in local:
			local[suburb]['medianAge'] = int(row[1])
			local[suburb]['medianMortgage'] = int(row[2])
			local[suburb]['medianSalary'] = int(row[3])
			local[suburb]['medianRent'] = float(row[4])
			local[suburb]['familySalary'] = int(row[5])
			local[suburb]['averagePersons'] = float(row[7])

# precess foi data
with open('foi.csv','r') as csvfile:
	reader = csv.reader(csvfile,delimiter=',')
	for row in reader:
		suburb = row[0]
		if suburb in local:
			local[suburb][row[2]] = 0
	# go back to the start of the file
	csvfile.seek(0)
	for row in reader:
		suburb = row[0]
		if suburb in local:
			local[suburb][row[2]] += 1
			

print local['3000']