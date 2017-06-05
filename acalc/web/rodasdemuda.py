# -*- coding: utf-8 -*-
__author__	= 'Daniel Oliveira'
__contact__	= 'danielfilipe.mo@gmail.com'
__date__	= '14 March 2017'

import cherrypy
from acalc.tools.common import  render_template
from acalc.tools.rodasdemuda import *

class RolletePage():
	@cherrypy.expose
	def index(self):
		return render_template("rodas_rollete.html")

	@cherrypy.expose
	def result(self, **kwargs):
		self._artigo	= kwargs.get('artigo', None)
		self._m 		= float(kwargs.get('modulo', None))
		self._b 		= str(kwargs.get('beta', 0))
		self._result 	= []
		if self._b != None and self._m != None:
			self._rollete 	= Rollete(modulo = self._m, beta = self._b)
			self._result 	= self._rollete.rodasdemuda()
			self._razaot 	= self._rollete._razao
			self._values 	= "<strong>Artigo:</strong> {} [n] [n]".format(self._artigo)
			self._values 	= self._values+"<strong>Razão Teórica:</strong> {0:.12f} [n]<strong>Módulo:</strong> {1} mm [n]<strong>Beta:</strong> {2}".format(self._razaot, self._m, self._b)
			return render_template("rodas_rollete.html",
				modulo 		= self._m,
				beta 		= self._b,
				resultados 	= self._result,
				artigo 		= self._artigo,
				values 		= self._values)
		else:
			return self.index()

class ReishauerPage():
	@cherrypy.expose
	def index(self):
		return render_template("rodas_reishauer.html")

	@cherrypy.expose
	def result(self, **kwargs):
		self._artigo	= kwargs.get('artigo', None)
		self._m 		= float(kwargs.get('modulo', None))
		self._b 		= str(kwargs.get('beta', 0))
		self._sentido 	= str(kwargs.get('radio', None)).upper()
		self._result 	= []
		if self._b != None and self._m != None and self._sentido != None:
			self.reishauer	= Reishauer(modulo = self._m, beta = self._b, sentido = self._sentido)
			self._result 	= self.reishauer.rodasdemuda()
			self._razaot 	= self.reishauer._razao
			self._values 	= "<strong>Artigo:</strong> {} [n] [n]".format(self._artigo)
			self._values 	= self._values+"<strong>Razão Teórica:</strong> {0:.12f} [n]<strong>Módulo:</strong> {1} mm [n]<strong>Beta:</strong> {2}[n]<strong>Sentido:</strong> {3}".format(self._razaot, self._m, self._b, self._sentido)
			return render_template("rodas_reishauer.html",
				modulo 		= self._m,
				beta 		= self._b,
				resultados 	= self._result,
				artigo 		= self._artigo,
				values 		= self._values)
		else:
			return self.index()

class DressagePage():
	@cherrypy.expose
	def index(self):
		return render_template("rodas_dressage.html")

	@cherrypy.expose
	def result(self, **kwargs):
		self._artigo	= kwargs.get('artigo', None)
		self._m 		= float(kwargs.get('modulo', None))
		self._result 	= []
		if self._m != None:
			self.dressage 	= ReishauerDressage(modulo = self._m)
			self._result 	= self.dressage.rodasdemuda()
			self._razaot 	= self.dressage._razao
			self._values 	= "<strong>Artigo:</strong> {} [n] [n]".format(self._artigo)
			self._values 	= self._values+"<strong>Razão Teórica:</strong> {0:.12f} [n]<strong>Módulo:</strong> {1} mm".format(self._razaot, self._m)
			return render_template("rodas_dressage.html",
				modulo 		= self._m,
				resultados 	= self._result,
				artigo 		= self._artigo,
				values 	= self._values)
		else:
			return self.index()

class P251Page():
	@cherrypy.expose
	def index(self):
		return render_template("rodas_p251.html")

	@cherrypy.expose
	def result(self, **kwargs):
		self._artigo	= kwargs.get('artigo', None)
		self._m 		= float(kwargs.get('modulo', 0))
		self._b 		= str(kwargs.get('beta', 0))
		self._entradas 	= int(kwargs.get('entradas', 0))
		self._modo 		= str(kwargs.get('radio', None)).upper()
		self._result 	= []
		if self._b != None and self._m != None and self._modo != None:
			self.p251 		= Pfauter251(modulo = self._m, beta = self._b, modo = self._modo, entradas = self._entradas)
			self._result 	= self.p251.rodasdemuda()
			self._razaot 	= self.p251._razao
			self._values 	= "<strong>Artigo:</strong> {} [n] [n]".format(self._artigo)
			self._values 	= self._values+"<strong>Razão Teórica:</strong> {0:.12f} [n]<strong>Módulo:</strong> {1} mm".format(self._razaot, self._m)
			if self._b != 0:
				self._values = self._values+"[n]<strong>Beta:</strong> {}".format(self._b)
			self._values 	= self._values+"[n]<strong>Entradas:</strong> {}[n]<strong>Modo:</strong> {}".format(self._entradas, self._modo)
			return render_template("rodas_p251.html",
				modulo 		= self._m,
				beta 		= self._b,
				entradas 	= self._entradas,
				resultados 	= self._result,
				artigo 		= self._artigo,
				values 		= self._values)
		else:
			return self.index()

class P630Page():
	@cherrypy.expose
	def index(self):
		return render_template("rodas_p630.html")

	@cherrypy.expose
	def result(self, **kwargs):
		self._artigo	= kwargs.get('artigo', None)
		self._m 		= float(kwargs.get('modulo', 0))
		self._b 		= str(kwargs.get('beta', 0))
		self._entradas 	= int(kwargs.get('entradas', 0))
		self._modo 		= str(kwargs.get('radio', None)).upper()
		self._result 	= []
		if self._b != None and self._m != None and self._modo != None:
			self.p630 		= Pfauter630(modulo = self._m, beta = self._b, modo = self._modo, entradas = self._entradas)
			self._result 	= self.p630.rodasdemuda()
			self._razaot 	= self.p630._razao
			self._values 	= "<strong>Artigo:</strong> {} [n] [n]".format(self._artigo)
			self._values 	= self._values+"<strong>Razão Teórica:</strong> {0:.12f}[n]<strong>Módulo:</strong> {1} mm".format(self._razaot, self._m)
			if self._b != 0:
				self._values = self._values+"[n]<strong>Beta:</strong> {}".format(self._b)
			self._values 	= self._values+"[n]<strong>Entradas:</strong> {}[n]<strong>Modo:</strong> {}".format(self._entradas, self._modo)
			return render_template("rodas_p630.html",
				modulo 		= self._m,
				beta 		= self._b,
				entradas 	= self._entradas,
				resultados 	= self._result,
				artigo 		= self._artigo,
				values 		= self._values)
		else:
			return self.index()

class P2300Page():
	@cherrypy.expose
	def index(self):
		return render_template("rodas_p2300.html")

	@cherrypy.expose
	def result(self, **kwargs):
		self._artigo	= kwargs.get('artigo', None)
		self._m 		= float(kwargs.get('modulo', 0))
		self._b 		= str(kwargs.get('beta', 0))
		self._entradas 	= int(kwargs.get('entradas', 0))
		self._modo 		= str(kwargs.get('radio', None)).upper()
		self._result 	= []
		if self._b != None and self._m != None and self._modo != None:
			self.p2300 		= Pfauter2300(modulo = self._m, beta = self._b, modo = self._modo, entradas = self._entradas)
			self._result 	= self.p2300.rodasdemuda()
			self._razaot 	= self.p2300._razao
			self._values 	= "<strong>Artigo:</strong> {} [n] [n]".format(self._artigo)
			self._values 	= self._values+"<strong>Razão Teórica:</strong> {0:.12f}[n]<strong>Módulo:</strong> {1} mm".format(self._razaot, self._m)
			if self._b != 0:
				self._values = self._values+"[n]<strong>Beta:</strong> {}".format(self._b)
			self._values 	= self._values+"[n]<strong>Entradas:</strong> {}[n]<strong>Modo:</strong> {}".format(self._entradas, self._modo)
			return render_template("rodas_p2300.html",
				modulo 		= self._m,
				beta 		= self._b,
				entradas 	= self._entradas,
				resultados 	= self._result,
				artigo 		= self._artigo,
				values 		= self._values)
		else:
			return self.index()

class ModulPage():
	@cherrypy.expose
	def index(self):
		return render_template("rodas_modul.html")

	@cherrypy.expose
	def result(self, **kwargs):
		self._artigo	= kwargs.get('artigo', None)
		self._m 		= float(kwargs.get('modulo', 0))
		self._b 		= str(kwargs.get('beta', 0))
		self._entradas 	= int(kwargs.get('entradas', 0))
		self._modo 		= str(kwargs.get('radio', None)).upper()
		self._result 	= []
		if self._b != None and self._m != None and self._modo != None:
			self.modul 		= Modul(modulo = self._m, beta = self._b, modo = self._modo, entradas = self._entradas)
			self._result 	= self.modul.rodasdemuda()
			self._razaot 	= self.modul._razao
			self._values 	= "<strong>Artigo:</strong> {} [n] [n]".format(self._artigo)
			self._values 	= self._values+"<strong>Razão Teórica:</strong> {0:.12f}[n]<strong>Módulo:</strong> {1} mm".format(self._razaot, self._m)
			if self._b != 0:
				self._values = self._values+"[n]<strong>Beta:</strong> {}".format(self._b)
			self._values 	= self._values+"[n]<strong>Entradas:</strong> {}[n]<strong>Modo:</strong> {}".format(self._entradas, self._modo)
			return render_template("rodas_modul.html",
				modulo 		= self._m,
				beta 		= self._b,
				entradas 	= self._entradas,
				resultados 	= self._result,
				artigo 		= self._artigo,
				values 		= self._values)
		else:
			return self.index()

class LindnerPage():
	@cherrypy.expose
	def index(self):
		return render_template("rodas_lindner.html")

	@cherrypy.expose
	def result(self, **kwargs):
		self._artigo	= kwargs.get('artigo', None)
		self._m 		= float(kwargs.get('modulo', 0))
		self._entradas 	= int(kwargs.get('entradas', 0))
		self._result 	= []
		if self._m != None:
			self.lindner = Lindner(modulo = self._m, entradas = self._entradas)
			self._result = self.lindner.rodasdemuda()
			self._razaot = self.lindner._razao
			self._values = "<strong>Artigo:</strong> {} [n] [n]".format(self._artigo)
			self._values 	= self._values+"<strong>Razão Teórica:</strong> {0:.12f}[n]<strong>Módulo:</strong> {1} mm[n]<strong>Entradas:</strong> {2}".format(self._razaot, self._m, self._entradas)
			return render_template("rodas_lindner.html",
				modulo 		= self._m,
				entradas 	= self._entradas,
				resultados 	= self._result,
				artigo 		= self._artigo,
				values 		= self._values)
		else:
			return self.index()

class HeckertPage():
	@cherrypy.expose
	def index(self):
		return render_template("rodas_heckert.html")

	@cherrypy.expose
	def result(self, **kwargs):
		self._artigo	= kwargs.get('artigo', None)
		self._m 		= float(kwargs.get('modulo', 0))
		self._entradas 	= int(kwargs.get('entradas', 0))
		self._result 	= []
		if self._m != None:
			self.heckert = Heckert(modulo = self._m, entradas = self._entradas)
			self._result = self.heckert.rodasdemuda()
			self._razaot = self.heckert._razao
			self._values = "<strong>Artigo:</strong> {} [n] [n]".format(self._artigo)
			self._values 	= self._values+"<strong>Razão Teórica:</strong> {0:.12f}[n]<strong>Módulo:</strong> {1} mm[n]<strong>Entradas:</strong> {2}".format(self._razaot, self._m, self._entradas)
			return render_template("rodas_heckert.html",
				modulo 		= self._m,
				entradas 	= self._entradas,
				resultados 	= self._result,
				artigo 		= self._artigo,
				values 		= self._values)
		else:
			return self.index()

class SpiromaticPage():
	@cherrypy.expose
	def index(self):
		return render_template("rodas_spiromatic.html")

	@cherrypy.expose
	def result(self, **kwargs):
		self._artigo	= kwargs.get('artigo', None)
		self._w 		= float(kwargs.get('razao', 0))
		self._modo 		= str(kwargs.get('radio', 0))
		self._result 	= []
		if self._w != None:
			self.spiromatic	= Spiromatic(w = self._w)
			if self._modo == "6rodas":
				self._result 	= self.spiromatic.rodasdemuda6()
			elif self._modo == "4rodas":
				self._result 	= self.spiromatic.rodasdemuda()

			self._values 	= "<strong>Artigo:</strong> {} [n] [n]".format(self._artigo)
			self._values 	= self._values+"<strong>Razão Teórica:</strong> {0:.12f}".format(self._w)
			return render_template("rodas_spiromatic.html",
									razao 			= self._w,
									resultados 	= self._result,
									artigo 		= self._artigo,
									values 		= self._values)
		else:
			return self.index()



class RodasPage:
	def __init__(self):
		self.rollete		= RolletePage()
		self.reishauer	= ReishauerPage()
		self.dressage	= DressagePage()
		self.p251		= P251Page()
		self.p630		= P630Page()
		self.p2300		= P2300Page()
		self.modul		= ModulPage()
		self.lindner		= LindnerPage()
		self.heckert	= HeckertPage()
		self.spiromatic	= SpiromaticPage()

	@cherrypy.expose
	def index(self):
		return render_template("rodasdemuda.html")


