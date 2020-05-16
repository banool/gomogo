#+----------------------------------------------------------------------------+
#|           author: Bobby Koteski - last update: 30/7/2016                   |
#+----------------------------------------------------------------------------+ 

#script imports
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json
import csv
import re
import SuburbData

#script constants / port 80 for server, 8080 for localhost
PORT_NUMBER = 8080

# dictionary to store csv data into program memory
local = SuburbData.get_data()

#This class will handles any incoming request from browser
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
			obj = json.dumps(data,indent=4)
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
