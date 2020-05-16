#!myvenv/bin/python

#+----------------------------------------------------------------------------+
#|           author: Bobby Koteski - last update: 30/7/2016                   |
#+----------------------------------------------------------------------------+ 

#script imports
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from urlparse import urlparse, parse_qs
import json
import os
import re
from dataGatherer import readPostcodeData
from random import randint

local = readPostcodeData()

PORT_NUMBER = int(os.getenv("BACKEND_PORT", 5001))

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
				try:
					postcode = int(postcode)
				except:
					pass
				print(postcode)
				if postcode in local:
					# This is the old line for sending back multiple postcodes at once:
					# data[postcode] = local[postcode].createFullDict()
					data = local[postcode].createFullDict()

			data = json.dumps(data) # Just getting one postcode.

			self.standard_response()
			self.wfile.write(data)

		else:
			self.invalidrequest()		
		return

	
	def do_POST(self):
		data = None
		while data is None or len(data) < 2:
			postcode = randint(3000, 3999)
			print("Trying postcode", postcode)
			try:
				data = local[postcode].createFullDict()
			except KeyError:
				data = None
		print(len(data))
		data = json.dumps(data)
		self.standard_response()
		self.wfile.write(data)
	

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
