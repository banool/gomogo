#+----------------------------------------------------------------------------+
#|           author: Bobby Koteski - last update: 30/7/2016                   |
#+----------------------------------------------------------------------------+ 

import csv

def get_data():
	# dictionary to store csv data into program memory
	local = {}

	# load suburb names into local memory
	with open('suburbnames.csv','r') as csvfile:
		reader = csv.reader(csvfile,delimiter=',')
		for row in reader:
			local[row[2]] = {'suburb' : row[1]}

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
			# parse suburb, format: POA3xxx
			suburb = row[0][3:]
			if suburb in local:
				local[suburb]['median age'] = int(row[1])
				local[suburb]['median mortgage'] = int(row[2])
				local[suburb]['median salary'] = int(row[3])
				local[suburb]['medianr rent'] = float(row[4])
				local[suburb]['family salary'] = int(row[5])
				local[suburb]['average persons'] = float(row[7])

	# precess foi data
	with open('foi.csv','r') as csvfile:
		reader = csv.reader(csvfile,delimiter=',')
		for row in reader:
			suburb = row[0]
			if suburb in local:
				local[suburb][row[2]] = 0
		# go back to the start of the file
		csvfile.seek(0)
		# count the feature occurences
		for row in reader:
			suburb = row[0]
			if suburb in local:
				local[suburb][row[2]] += 1

	return local
