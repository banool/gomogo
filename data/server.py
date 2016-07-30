#+----------------------------------------------------------------------------+
#|           author: Bobby Koteski - last update: 30/7/2016                   |
#+----------------------------------------------------------------------------+ 

#script imports
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from urlparse import urlparse, parse_qs
import json
import csv
import re

#script constants / port 80 for server, 8080 for localhost
PORT_NUMBER = 80

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

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

	#print welcome messege to server
	def welcome(self):
		self.standard_response()
		# Send the html message
		self.wfile.write('Welcome to GovHack2016!')

	# standard code block to handle each response
	def standard_response(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		print self.headers.getheader('Content-type')

	# json test response
	def jsontest(self):
		self.standard_response()
		data = { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 }
		obj = json.dumps(data)
		self.wfile.write(obj)

	def invalidrequest(self):
		self.standard_response()
		self.wfile.write('Error! You have submitted an invalid request.')

	#Handler for the GET requests
	def do_GET(self):

		# parse the url for postcodes if they exist
		requests = re.findall('\w{4}',self.path)
		
		if self.path == '/':
			self.welcome()
		elif self.path == '/jsontest':
			self.jsontest()
		elif len(requests) > 0:
			data = {}
			for postcode in requests:
				if postcode in local:
					data[postcode] = local[postcode]
			obj = json.dumps(data)
			self.standard_response()
			self.wfile.write(obj)
		else:
			self.invalidrequest()		
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server!'
	server.socket.close()
