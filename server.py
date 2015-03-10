#!/usr/bin/env python

import BaseHTTPServer
import gevent
import sys
import time
import os

from ouimeaux.environment import Environment, UnknownDevice
from ouimeaux.utils import matcher
from ouimeaux.signals import statechange, receiver, devicefound

lightOn = False

matches = matcher("LAX Beerlight")

curdir = os.path.dirname(os.path.realpath(__file__))

@receiver(devicefound)
def found(sender, **kwargs):
		if matches(sender.name):
				print "Found beerlight!"

env = Environment(with_cache=False,bind="192.168.101.13:54321")

						
try:
	print "Starting wemo server."

	env.start()

	print "Discovering devices"
	env.discover(10)
	
	try:
		switch = env.get_switch("LAX Beerlight")
	except UnknownDevice:
		print "Beerlight not detected, please try again.\nIf error persists do 'wemo clear; wemo -b 192.168.101.13:54321 list'.\nIf an exception occurs keep re-running this until the error clears."
		sys.exit(1)

	
	print "Starting webserver on port 80"

	class Handler( BaseHTTPServer.BaseHTTPRequestHandler ):
		def do_GET( self ):

			if self.path=="/toggle":
				switch = env.get_switch("LAX Beerlight")
				state = switch.basicevent.GetBinaryState()
				if state["BinaryState"]=="1":
					switch.basicevent.SetBinaryState(BinaryState=0)
				else:
					switch.basicevent.SetBinaryState(BinaryState=1)

				self.send_response(302)
				self.send_header('Location', '/')
				self.end_headers()
				
				return
			
			if self.path=="/":
				switch = env.get_switch("LAX Beerlight")
				self.send_response(200)
				self.send_header('Content-type', 'text/html' )
				self.end_headers()
				state = switch.basicevent.GetBinaryState()
				if state["BinaryState"]=="1":
					self.wfile.write( open('beer-on.html').read() )
				else:
					self.wfile.write( open('beer-off.html').read() )
				return
			try:
				if self.path.endswith(".png"):
					mimetype="image/png"
				f = open(curdir + self.path,"rb")
				self.send_response(200)
				self.send_header('Content-type', mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
				return
			except IOError:
				self.send_error(404, "File Not Found: %s" % self.path)

	try:
		httpd = BaseHTTPServer.HTTPServer( ('10.0.100.10', 80), Handler )
		httpd.serve_forever()
	except IOError:
		print "Failed to bind to port 80, are you running as sudo?"
		sys.exit(1)

except (KeyboardInterrupt, SystemExit):
	sys.exit(0)
