# -*- coding: utf-8 -*-
__author__	= 'Daniel Oliveira'
__contact__	= 'danielfilipe.mo@gmail.com'
__date__	= '31 March 2013'

import cherrypy
from acalc.tools.common import  render_template
from .rodasdemuda import RodasPage
from .cotas import CotasPage
from .calculos import CalcPage

class RootServer:
	def __init__(self):
		self.rodasdemuda	=	RodasPage()
		self.cotas			=	CotasPage()
		self.calculos		=	CalcPage()
		
	@cherrypy.expose
	def index(self,):
		return render_template("index.html")
		
		
		