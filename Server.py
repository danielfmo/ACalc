#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__	= 'Daniel Oliveira'
__contact__	= 'danielfilipe.mo@gmail.com'
__date__	= '31 March 2013'

import sys
import logging
from logging import handlers
import os
from os import path

import cherrypy
from cherrypy import _cplogging
from cherrypy.lib import httputil

class Server():
	def __init__(self):
		# Our Root directory
		self.base_dir = path.dirname(path.abspath(sys.argv[0]))
		# Our conf directory
		self.conf_path = path.join(self.base_dir, "conf")
		# Our Static directory
		self.static_dir = path.join(self.base_dir, "acalc", 'static')

		# Update the global settings for the HTTP server and engine
		cherrypy.config.update(path.join(self.conf_path, "server.ini"))
		
		self.engine = cherrypy.engine
		
		# We amend the system path so that Python can find
		# the application's modules.
		sys.path.insert(0, self.base_dir)

		# Our application
		from acalc.web.root import RootServer
		webapp = RootServer()
		
		# Let's mount the application so that CherryPy can serve it
		app = cherrypy.tree.mount(webapp, '/', path.join(self.conf_path, "acalc.ini"))
		self.logs(app)

	def run(self):
		#self.engine = cherrypy.engine
		self.engine.start()
		self.engine.block()		
		
	def logs(self, app):
		# see http://www.cherrypy.org/wiki/Logging#CustomHandlers
		log = app.log
		log.error_file = ""
		log.access_file = None
		#log.access_file = ""

		maxBytes = getattr(log, "rot_maxBytes", 10485760)
		backupCount = getattr(log, "rot_backupCount", 5)

		# LOG LEVELS (default = WARNING)
		# DEBUG		-	Detailed information, typically of interest only when diagnosing problems.
		# INFO		-	Confirmation that things are working as expected.
		# WARNING	-	An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
		# ERROR		-	Due	to a more serious problem, the software has not been able to perform some function.
		# CRITICAL	-	A serious error, indicating that the program itself may be unable to continue running.		
		
		# Make a new RotatingFileHandler for the error log.
		fname = getattr(log, "rot_error_file", "./logs/error.log")
		h = handlers.RotatingFileHandler(fname, 'a', maxBytes, backupCount)
		h.setLevel(logging.ERROR)
		h.setFormatter(_cplogging.logfmt)
		log.error_log.addHandler(h)

		# Make a new RotatingFileHandler for the access log.
		#fname = getattr(log, "rot_access_file", "./logs/access.log")
		#h = handlers.RotatingFileHandler(fname, 'a', maxBytes, backupCount)
		#h.setLevel(logging.DEBUG)
		#h.setFormatter(_cplogging.logfmt)
		#log.access_log.addHandler(h)		
		
if __name__ == '__main__':
	Server().run()


