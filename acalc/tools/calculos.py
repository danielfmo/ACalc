# -*- coding: utf-8 -*-
__author__	= 'Daniel Oliveira'
__contact__	= 'danielfilipe.mo@gmail.com'
__date__	= '31 March 2013'

from math import fabs, sin, cos, tan, atan, ceil, pi, pow, sqrt, degrees, radians

class CalcSpiro (object):
	def __init__ (self) :
		self._semething		= 0

	def passo1(self, kwargs):
		self._sentido		= str(kwargs.get('radio1', None)).upper()
		self._m				= float(kwargs.get('modulo', None))
		self._z1 			= int(kwargs.get('z1', None))
		self._z2 			= int(kwargs.get('z2', None))
		self._e 			= float(kwargs.get('e', None))
		self._alfa 			= float(kwargs.get('alfa', None))
		
		self._D1 = self._m*self._z1
		self._D2 = self._m*self._z2
		self._zp = sqrt(	pow(self._z1, 2) + pow((self._z2+self._z1*cos(radians(self._e)))/sin(radians(self._e)), 2)	)
		
		self._S1 = atan(	(self._z1/self._zp)/sqrt(-pow(self._z1/self._zp, 2)+1)	)
		self._S2 = atan(	(self._z2/self._zp)/sqrt(-pow(self._z2/self._zp, 2)+1)	)

		self._R = self._D2/(2*sin(self._S2))
		self._b = 0.285*self._R

		self._S1 = degrees(self._S1)
		self._S2 = degrees(self._S2)
		
		return self
		
		
		
		
		
		
		
		
		
		
		
		
		
		