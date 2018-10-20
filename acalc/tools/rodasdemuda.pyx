# -*- coding: utf-8 -*-
__author__	= 'Daniel Oliveira'
__contact__	= 'danielfilipe.mo@gmail.com'
__date__	= '31 March 2013'

from libcpp.vector cimport vector
from libc.math cimport fabs, sin, cos
from math import pi, degrees, radians
from operator import itemgetter
from itertools import groupby
from .common import six2dec
# modulo, beta
class Rollete (object):
	def __init__ (self, **kwargs) :
		self._name 			= 'rollete'
		self._modelo 		= 'Runderland 5A-4C'
		self._conj_rodas 	= (27,28,30,30,32,33,35,36,38,39,40,40,40,42,42,44,45,46,48,48,50,51,52,53,54,55,56,57,58,59,60,60,60,61,62,63,64,65,67,68,70,71,72,73,74,75,76,79,82,83,84,86,89,93,94,96,97,100,105,107,108,110,120,127)
		self._m 				= kwargs.get('modulo', None)
		self._beta 			= kwargs.get('beta', 0)
		self._beta 			= radians(six2dec(self._beta))
		self._razao 			= self._m/(4.5*cos(self._beta)) 	#modulo e beta
		
	def limites(self, *conjunto):
		if len(conjunto) != 4:
			return None
		else :
			A = conjunto[0]
			B = conjunto[1]
			C = conjunto[2]
			D = conjunto[3]

		MAX_AB	=	120			# A+B <=
		MAX_CD	=	135			# C+D <=                                                                                                            
		MIN_AB	=	78			# A+B >= 
		MIN_CD	=	88			# C+D >= 
	
		if A+B<=MAX_AB and C+D<=MAX_CD and A+B>=MIN_AB and C+D>=MIN_CD:
			return True
		else:
			return False	
			
	def rodasdemuda(self, float erro = 0.001):
		cdef float razaom, err
		razaom = 0
		err = 0
		
		cdef int lrodas, a, b, c, d
		a = 0
		b = 0
		c = 0
		d = 0
		lrodas = len (self._conj_rodas)
		
		cdef vector[float] rodas = self._conj_rodas

		result = []

		for a from 0 <= a < lrodas:
			for b from 0 <= b < lrodas:
				for c from 0 <= c < lrodas:
					for d from 0 <= d < lrodas:
						razaom=rodas[a]/rodas[b]*rodas[c]/rodas[d]
						err = fabs (self._razao - razaom)
						if err<=erro and (a!=b and a!=c and a!=d and b!=c and b!=d and c!=d):
							if self.limites(rodas[a], rodas[b], rodas[c], rodas[d]):
								result.append(dict (A=rodas[a], B=rodas[b], C=rodas[c], D=rodas[d], erro=err, razaom=razaom))

		#remove resultados com conjuntos duplicados devido a existirem rodas de muda iguais
		keyfunc = lambda d: (d['A'], d['B'], d['C'], d['D'])
		giter = groupby(sorted(result, key=keyfunc), keyfunc)
		result = [next(g[1]) for g in giter]
		
		#ordena os resultados pelo erro, ascendente
		result = sorted(result, key=itemgetter('erro'))
		
		#limita o numero de resultados a 12
		if len(result) > 12:	
			result = result[0:12]	
		
		return result

# modulo, beta, sentido
class Reishauer (object):
	def __init__ (self, **kwargs) :
		self._name 			= 'reishauer'
		self._modelo 		= 'reishauer'
		self._conj_rodas 	= (35,36,38,40,40,41,42,43,44,45,45,46,47,48,49,50,50,51,52,53,54,55,56,57,58,59,60,60,61,62,63,64,65,66,67,68,69,70,70,71,72,73,74,75,75,76,78,80,80,81,82,84,85,86,87,88,90,90,91,92,93,94,95,96,100,101,103,105,106,108,110,112,118,120)
		self._m 			= kwargs.get('modulo', None)
		self._beta 			= kwargs.get('beta', 0)
		self._beta 			= radians(six2dec(self._beta))
		self._sentido		= str(kwargs.get('sentido', None)).upper()
		self._razao 		= 11.6909*sin(self._beta)/self._m			#modulo e beta
		
	def limites(self, *conjunto):
		if len(conjunto) != 4:
			return None
		else :
			A = conjunto[0]
			B = conjunto[1]
			C = conjunto[2]
			D = conjunto[3]

		MAX_A	=	105			# A <= 
		MAX_B	=	C+D-34		# B <= 
		MAX_C	=	A+B-23		# C <= 
		MAX_D	=	120			# D <= 

		if A<=MAX_A and B<=MAX_B and C<=MAX_C and D<=MAX_D:
			if self._sentido == "ESQUERDA":
				MAX_AB	=	190			# A+B <=
				MAX_T	=	394			# A+B+C+D se A+B maximo
				MIN_AB	=	84			# A+B >=
				MIN_T_AB=	264			# A+B+C+D se A+B minimo					
				MIN_CD	=	90			# D+C >=
				MIN_T_CD=	229			# A+B+C+D se C+D minimo
				
				if ( A+B<=MAX_AB and A+B+C+D<=MAX_T ) and ( ( C+D>=MIN_CD and A+B+C+D>=MIN_T_CD ) or ( A+B>=MIN_AB and A+B+C+D>=MIN_T_AB ) ):
					return True
				else :
					return False

			elif self._sentido == "DIREITA":		
				MAX		=	193			# C+D <=
				MAX_T	=	383			# A+B+C+D se C+D maximo
				MIN		=	71			# C+D >=
				MIN_T	=	153			# A+B+C+D se C+D minimo
				
				if ( (C+D<=MAX) and (A+B+C+D<=MAX_T) ) and (C+D>=MIN) and (A+B+C+D>=MIN_T):
					return True
				else :
					return False

			else:
				return None		

			
	def rodasdemuda(self, float erro = 0.001):
		cdef float razaom, err
		razaom = 0
		err = 0
		
		cdef int lrodas, a, b, c, d
		a = 0
		b = 0
		c = 0
		d = 0
		lrodas = len (self._conj_rodas)
		
		cdef vector[float] rodas = self._conj_rodas

		result = []

		for a from 0 <= a < lrodas:
			for b from 0 <= b < lrodas:
				for c from 0 <= c < lrodas:
					for d from 0 <= d < lrodas:
						razaom=rodas[a]/rodas[b]*rodas[c]/rodas[d]
						err = fabs (self._razao - razaom)
						if err<=erro and (a!=b and a!=c and a!=d and b!=c and b!=d and c!=d):
							if self.limites(rodas[a], rodas[b], rodas[c], rodas[d]):
								result.append(dict (A=rodas[a], B=rodas[b], C=rodas[c], D=rodas[d], erro=err, razaom=razaom))

		#remove resultados com conjuntos duplicados devido a existirem rodas de muda iguais
		keyfunc = lambda d: (d['A'], d['B'], d['C'], d['D'])
		giter = groupby(sorted(result, key=keyfunc), keyfunc)
		result = [next(g[1]) for g in giter]
		
		#ordena os resultados pelo erro, ascendente
		result = sorted(result, key=itemgetter('erro'))
		
		#limita o numero de resultados a 12
		if len(result) > 12:	
			result = result[0:12]	
		
		return result
		
# Modulo
class ReishauerDressage (object):
	def __init__ (self, **kwargs) :
		self._name 			= 'reishauer_dressage'
		self._modelo 		= 'reishauer'
		self._conj_rodas 	= (35,36,38,40,40,41,42,43,44,45,45,46,47,48,49,50,50,51,52,53,54,55,56,57,58,59,60,60,61,62,63,64,65,66,67,68,69,70,70,71,72,73,74,75,75,76,78,80,80,81,82,84,85,86,87,88,90,90,91,92,93,94,95,96,100,101,103,105,106,108,110,112,118,120)
		self._m 			= kwargs.get('modulo', None)
		self._razao 		= self._razao = 6/25.4*self._m								#modulo
		
	def limites(self, *conjunto):
		if len(conjunto) != 4:
			return None
		else :
			A = conjunto[0]
			B = conjunto[1]
			C = conjunto[2]
			D = conjunto[3]

		MAX_A	=	60			# A <= 
		MAX_B	=	C+D-34		# C <= C+D-34
		MAX_C	=	A+B-23		# C <= A+B-23
		MAX_D	=	105			# D <= 
		MAX_AB	=	166			# A+B <=
		MAX_CD	=	145			# C+D <=                                                                                                           
		MAX_T	=	311			# A+B+C+D <= 
		MIN_AB	=	84			# A+B >= 
		MIN_T_AB=	229			# A+B+C+D se A+B minimo
		MIN_CD	=	108			# C+D >= 
		MIN_T_CD=	216			# A+B+C+D SE C+D minimo

		if A<=MAX_A and B<=MAX_B and C<=MAX_C and D<=MAX_D and A+B<=MAX_AB and A+B+C+D<=MAX_T and C+D<=MAX_CD and ( ( C+D>=MIN_CD and A+B+C+D>=MIN_T_CD ) or ( A+B>=MIN_AB and A+B+C+D>=MIN_T_AB ) ):
			return True
		else :
			return False
			
	def rodasdemuda(self, float erro = 0.001):
		cdef float razaom, err
		razaom = 0
		err = 0
		
		cdef int lrodas, a, b, c, d
		a = 0
		b = 0
		c = 0
		d = 0
		lrodas = len (self._conj_rodas)
		
		cdef vector[float] rodas = self._conj_rodas

		result = []

		for a from 0 <= a < lrodas:
			for b from 0 <= b < lrodas:
				for c from 0 <= c < lrodas:
					for d from 0 <= d < lrodas:
						razaom=rodas[a]/rodas[b]*rodas[c]/rodas[d]
						err = fabs (self._razao - razaom)
						if err<=erro and (a!=b and a!=c and a!=d and b!=c and b!=d and c!=d):
							if self.limites(rodas[a], rodas[b], rodas[c], rodas[d]):
								result.append(dict (A=rodas[a], B=rodas[b], C=rodas[c], D=rodas[d], erro=err, razaom=razaom))

		#remove resultados com conjuntos duplicados devido a existirem rodas de muda iguais
		keyfunc = lambda d: (d['A'], d['B'], d['C'], d['D'])
		giter = groupby(sorted(result, key=keyfunc), keyfunc)
		result = [next(g[1]) for g in giter]
		
		#ordena os resultados pelo erro, ascendente
		result = sorted(result, key=itemgetter('erro'))
		
		#limita o numero de resultados a 12
		if len(result) > 12:	
			result = result[0:12]	
		
		return result		
		
# modulo, entradas, modo ou beta
class Pfauter251 (object):
	def __init__ (self, **kwargs) :
		self._name 			= 'pfauter251'
		self._modelo 		= 'P251'
		self._conj_rodas 	= (20,21,22,23,24,24,25,25,26,27,27,28,29,29,30,31,32,32,33,34,35,36,36,37,38,38,39,40,40,41,42,42,43,44,45,45,46,47,48,48,49,50,51,52,53,54,55,56,57,58,58,59,60,60,61,62,63,64,64,65,66,67,68,69,70,71,71,72,72,73,74,75,76,77,78,79,80,81,82,83,84,86,87,88,89,92,94,95,96,97,98,101,102,103,107,109,113,127)
		self._m 				= kwargs.get('modulo', None)
		self._beta 			= kwargs.get('beta', 0)
		self._beta 			= radians(six2dec(self._beta))
		self._zO				= kwargs.get('entradas', None)
		self._modo 			= str(kwargs.get('modo', None)).upper()
		if self._modo == 'DIFERENCIAL':
			self._razao =(2.864789*sin(self._beta))/(self._m*self._zO)	#modulo, beta, entradas
		elif self._modo == 'TANGENCIAL':
			self._razao =(3*cos(self._beta))/(2*self._m*self._zO)		#modulo, beta, entradas
		elif self._modo == 'NAVALHAO':
			self._razao =3/(2*self._m*self._zO)									#modulo, beta, entradas, angulo a 0 para navalhão
		else :
			self._razao = None
			
	def limites(self, *conjunto):
		if len(conjunto) != 4:
			return None
		else :
			A = conjunto[0]
			B = conjunto[1]
			C = conjunto[2]
			D = conjunto[3]

		MAX_AB	=	170			# 
		MAX_CD	=	180			# 
		MIN_AB	=	80			# 
		MIN_CD	=	B+21 if B>=39 else 60	# C+D >= 60 and C+D>=B+21
		MAX_D	=	127			# 
	
		if A+B>=MIN_AB and A+B<=MAX_AB and C+D>=MIN_CD and C+D<=MAX_CD and D<=MAX_D:
			return True
		else :
			return False
			
	def rodasdemuda(self, float erro = 0.001):
		cdef float razaom, err
		razaom = 0
		err = 0
		
		cdef int lrodas, a, b, c, d
		a = 0
		b = 0
		c = 0
		d = 0
		lrodas = len (self._conj_rodas)
		
		cdef vector[float] rodas = self._conj_rodas

		result = []

		for a from 0 <= a < lrodas:
			for b from 0 <= b < lrodas:
				for c from 0 <= c < lrodas:
					for d from 0 <= d < lrodas:
						razaom=rodas[a]/rodas[b]*rodas[c]/rodas[d]
						err = fabs (self._razao - razaom)
						if err<=erro and (a!=b and a!=c and a!=d and b!=c and b!=d and c!=d):
							if self.limites(rodas[a], rodas[b], rodas[c], rodas[d]):
								result.append(dict (A=rodas[a], B=rodas[b], C=rodas[c], D=rodas[d], erro=err, razaom=razaom))

		#remove resultados com conjuntos duplicados devido a existirem rodas de muda iguais
		keyfunc = lambda d: (d['A'], d['B'], d['C'], d['D'])
		giter = groupby(sorted(result, key=keyfunc), keyfunc)
		result = [next(g[1]) for g in giter]
		
		#ordena os resultados pelo erro, ascendente
		result = sorted(result, key=itemgetter('erro'))
		
		#limita o numero de resultados a 12
		if len(result) > 12:	
			result = result[0:12]	
		
		return result
		
# modulo, entradas, modo ou beta
class Pfauter630 (object):
	def __init__ (self, **kwargs) :
		self._name 			= 'pfauter630'
		self._modelo 		= 'P630'
		self._conj_rodas 	= (20,21,22,23,24,24,25,25,26,27,27,28,29,29,30,31,32,32,33,34,35,36,36,37,38,38,39,40,40,41,42,42,43,44,45,45,46,47,48,48,49,50,51,52,53,54,55,56,57,58,58,59,60,60,61,62,63,64,64,65,66,67,68,69,70,71,71,72,72,73,74,75,76,77,78,79,80,81,82,83,84,86,87,88,89,92,94,95,96,97,98,101,102,103,107,109,113,127)
		self._m 			= kwargs.get('modulo', None)
		self._beta 			= kwargs.get('beta', 0)
		self._beta 			= radians(six2dec(self._beta))
		self._zO			= kwargs.get('entradas', None)
		self._modo 			= str(kwargs.get('modo', None)).upper()
		if self._modo == 'DIFERENCIAL':
			self._razao =(8.952466*sin(self._beta))/(self._m*self._zO)	#modulo, beta, entradas
		elif self._modo == 'TANGENCIAL':
			self._razao =(3*cos(self._beta))/(self._m*self._zO)			#modulo, beta, entradas, angulo a 0 para navalhão
		elif self._modo == 'NAVALHAO':
			self._razao =3/(self._m*self._zO)									#modulo, beta, entradas, angulo a 0 para navalhão
		else :
			self._razao = None
			
	def limites(self, *conjunto):
		if len(conjunto) != 4:
			return None
		else :
			A = conjunto[0]
			B = conjunto[1]
			C = conjunto[2]
			D = conjunto[3]

		MAX_AB	=	107						# 150 nos apontamentos
		MAX_CD	=	160						# 
		MIN_AB	=	50						# 
		MIN_CD	=	B+31 if B>=49 else 80	# C+D >= 80 and C+D>=B+31
		MAX_D	=	110						# 		
		#MAX_BC = 145						Existe no programa em PHP esta limitacao
	
		if A+B>=MIN_AB and A+B<=MAX_AB and C+D>=MIN_CD and C+D<=MAX_CD and D<=MAX_D:
			return True
		else :
			return False
			
	def rodasdemuda(self, float erro = 0.001):
		cdef float razaom, err
		razaom = 0
		err = 0
		
		cdef int lrodas, a, b, c, d
		a = 0
		b = 0
		c = 0
		d = 0
		lrodas = len (self._conj_rodas)
		
		cdef vector[float] rodas = self._conj_rodas

		result = []

		for a from 0 <= a < lrodas:
			for b from 0 <= b < lrodas:
				for c from 0 <= c < lrodas:
					for d from 0 <= d < lrodas:
						razaom=rodas[a]/rodas[b]*rodas[c]/rodas[d]
						err = fabs (self._razao - razaom)
						if err<=erro and (a!=b and a!=c and a!=d and b!=c and b!=d and c!=d):
							if self.limites(rodas[a], rodas[b], rodas[c], rodas[d]):
								result.append(dict (A=rodas[a], B=rodas[b], C=rodas[c], D=rodas[d], erro=err, razaom=razaom))

		#remove resultados com conjuntos duplicados devido a existirem rodas de muda iguais
		keyfunc = lambda d: (d['A'], d['B'], d['C'], d['D'])
		giter = groupby(sorted(result, key=keyfunc), keyfunc)
		result = [next(g[1]) for g in giter]
		
		#ordena os resultados pelo erro, ascendente
		result = sorted(result, key=itemgetter('erro'))
		
		#limita o numero de resultados a 12
		if len(result) > 12:	
			result = result[0:12]	
		
		return result

# modulo, entradas, modo ou beta
class Pfauter2300 (object):
	def __init__ (self, **kwargs) :
		self._name 			= 'pfauter2300'
		self._modelo 		= 'P2300'
		self._conj_rodas 	= (20,21,22,23,24,25,26,26,27,28,29,
									30,31,32,33,34,35,36,37,38,39,
									40,41,42,43,44,45,46,47,48,49,
									50,51,52,53,54,54,55,56,57,58,59,
									60,61,62,63,64,65,66,67,68,69,
									70,71,72,73,74,75,76,77,78,79,
									80,80,82,84,85,85,90,90)
		self._m 				= kwargs.get('modulo', None)
		self._beta 			= kwargs.get('beta', 0)
		self._beta 			= radians(six2dec(self._beta))
		self._zO				= kwargs.get('entradas', None)
		self._modo 			= str(kwargs.get('modo', None)).upper()
		if self._modo == 'DIFERENCIAL':
			self._razao = (12.732395*sin(self._beta))/(self._m*self._zO)	#modulo, beta, entradas
		elif self._modo == 'TANGENCIAL':
			self._razao = (8*cos(self._beta))/(3*self._m*self._zO)			#modulo, beta, entradas
		elif self._modo == 'NAVALHAO':
			self._razao = 8/(3*self._m*self._zO)									#modulo, beta, entradas, angulo a 0 para navalhão
		else :
			self._razao = None
			
	def limites(self, *conjunto):
		if len(conjunto) != 4:
			return None
		else :
			A = conjunto[0]
			B = conjunto[1]
			C = conjunto[2]
			D = conjunto[3]

			MAX_A	=	51	
			MAX_D	=	85	
			
			# From P630
			MAX_AB	=	107
			MAX_CD	=	160
			MIN_AB	=	50
			MIN_CD	=	B+31 if B>=49 else 80	# C+D >= 80 and C+D>=B+31

			if A+B>=MIN_AB and A+B<=MAX_AB and C+D>=MIN_CD and C+D<=MAX_CD and A<=MAX_A and D<=MAX_D:
				return True
			else :
				return False
			
	def rodasdemuda(self, float erro = 0.001):
		cdef float razaom, err
		razaom = 0
		err = 0
		
		cdef int lrodas, a, b, c, d
		a = 0
		b = 0
		c = 0
		d = 0
		lrodas = len (self._conj_rodas)
		
		cdef vector[float] rodas = self._conj_rodas

		result = []

		for a from 0 <= a < lrodas:
			for b from 0 <= b < lrodas:
				for c from 0 <= c < lrodas:
					for d from 0 <= d < lrodas:
						razaom=rodas[a]/rodas[b]*rodas[c]/rodas[d]
						err = fabs (self._razao - razaom)
						if err<=erro and (a!=b and a!=c and a!=d and b!=c and b!=d and c!=d):
							if self.limites(rodas[a], rodas[b], rodas[c], rodas[d]):
								result.append(dict (A=rodas[a], B=rodas[b], C=rodas[c], D=rodas[d], erro=err, razaom=razaom))

		#remove resultados com conjuntos duplicados devido a existirem rodas de muda iguais
		keyfunc = lambda d: (d['A'], d['B'], d['C'], d['D'])
		giter = groupby(sorted(result, key=keyfunc), keyfunc)
		result = [next(g[1]) for g in giter]
		
		#ordena os resultados pelo erro, ascendente
		result = sorted(result, key=itemgetter('erro'))
		
		#limita o numero de resultados a 12
		if len(result) > 12:	
			result = result[0:12]	
		
		return result
		
# modulo, entradas, modo ou beta
class Modul (object):
	def __init__ (self, **kwargs) :
		self._name 			= 'Modul'
		self._modelo 		= '250x5'
		self._conj_rodas 	= (20,21,22,22,23,24,25,26,26,27,28,29,29,29,30,30,31,32,33,34,35,36,36,37,38,39,40,40,41,42,43,44,45,45,46,47,47,48,48,49,50,50,51,52,53,54,55,56,57,58,59,60,60,61,62,62,63,64,65,66,67,67,68,69,70,70,71,71,72,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,89,90,91,92,94,95,96,97,98,100,101,103,105,109,110,120)
		self._m 			= kwargs.get('modulo', None)
		self._beta 			= kwargs.get('beta', 0)
		self._beta 			= radians(six2dec(self._beta))
		self._zO			= kwargs.get('entradas', None)
		self._modo 			= str(kwargs.get('modo', None)).upper()
		if self._modo == 'DIFERENCIAL':
			self._razao = (6*sin(self._beta))/(self._m*self._zO)		#modulo, beta, entradas
		elif self._modo == 'TANGENCIAL':
			self._razao = (3*cos(self._beta))/(self._m*self._zO)	
		elif self._modo == 'NAVALHAO':
			self._razao = 3/(self._m*self._zO)								#modulo, entradas
		else :
			self._razao = None
			
	def limites(self, *conjunto):
		if len(conjunto) != 4:
			return None
		else :
			A = conjunto[0]
			B = conjunto[1]
			C = conjunto[2]
			D = conjunto[3]

		# existe a possibilidade de colocar as rodas de muda em "linha" ou introduzir uma ou duas rodas intermediarias
		# nestas situacoes os limites sao diferentes e apenas podem ser confirmados graficamente
		# Neste caso desprezo as situacoes anteriores tentando colocar limites o maas universais possiveis
		MAX_AB	=	194
		MIN_AB	=	77
		MAX_CD	=	200						# para permitir uma roda intermediaria
		MIN_CD	=	B+24 if B>=46 else 70 	# C+D >= 70 and C+D>=B+24
		MAX_A	=	100
		MAX_D	=	120

		if A+B>=MIN_AB and A+B<=MAX_AB and C+D>=MIN_CD and C+D<=MAX_CD and A<=MAX_A and D<=MAX_D:
			return True
		else :
			return False
			
	def rodasdemuda(self, float erro = 0.001):
		cdef float razaom, err
		razaom = 0
		err = 0
		
		cdef int lrodas, a, b, c, d
		a = 0
		b = 0
		c = 0
		d = 0
		lrodas = len (self._conj_rodas)
		
		cdef vector[float] rodas = self._conj_rodas

		result = []

		for a from 0 <= a < lrodas:
			for b from 0 <= b < lrodas:
				for c from 0 <= c < lrodas:
					for d from 0 <= d < lrodas:
						razaom=rodas[a]/rodas[b]*rodas[c]/rodas[d]
						err = fabs (self._razao - razaom)
						if err<=erro and (a!=b and a!=c and a!=d and b!=c and b!=d and c!=d):
							if self.limites(rodas[a], rodas[b], rodas[c], rodas[d]):
								result.append(dict (A=rodas[a], B=rodas[b], C=rodas[c], D=rodas[d], erro=err, razaom=razaom))

		#remove resultados com conjuntos duplicados devido a existirem rodas de muda iguais
		keyfunc = lambda d: (d['A'], d['B'], d['C'], d['D'])
		giter = groupby(sorted(result, key=keyfunc), keyfunc)
		result = [next(g[1]) for g in giter]
		
		#ordena os resultados pelo erro, ascendente
		result = sorted(result, key=itemgetter('erro'))
		
		#limita o numero de resultados a 12
		if len(result) > 12:	
			result = result[0:12]	
		
		return result
		
# Modulo e entradas		
class Lindner (object):
	def __init__ (self, **kwargs) :
		self._name 			= 'Lindner'
		self._modelo 		= 'LINDNER'
		self._conj_rodas	= (24,27,30,30,32,33,34,36,39,40,42,45,45,47,48,48,51,52,54,58,60,60,60,63,65,65,66,68,70,70,70,72,75,75,76,80,86,90,90,91,94,95,96,100,104,110,120,120,127)	
		self._m 			= kwargs.get('modulo', None)
		self._zO			= kwargs.get('entradas', None)
		if self._m<=2:
			self._razao = 6*pi/25.4*self._m*self._zO					
		else :
			self._razao = (6*pi)/(25.4*12)*self._m*self._zO				
			
	def limites(self, *conjunto):
		if len(conjunto) != 4:
			return None
		else :
			A = conjunto[0]
			B = conjunto[1]
			C = conjunto[2]
			D = conjunto[3]

		MAX_A	=	100
		MAX_B	=	100
		MAX_D	=	120
		MAX_AB	=	194
		MIN_CD	=	B+33 if B>=27 else 60 	# C+D >= 60 and C+D>=B+33

		if A+B<=MAX_AB and C+D>=MIN_CD and A<=MAX_A and B<=MAX_B and D<=MAX_D:
			return True
		else :
			return False
			
	def rodasdemuda(self, float erro = 0.001):
		cdef float razaom, err
		razaom = 0
		err = 0
		
		cdef int lrodas, a, b, c, d
		a = 0
		b = 0
		c = 0
		d = 0
		lrodas = len (self._conj_rodas)
		
		cdef vector[float] rodas = self._conj_rodas

		result = []

		for a from 0 <= a < lrodas:
			for b from 0 <= b < lrodas:
				for c from 0 <= c < lrodas:
					for d from 0 <= d < lrodas:
						razaom=rodas[a]/rodas[b]*rodas[c]/rodas[d]
						err = fabs (self._razao - razaom)
						if err<=erro and (a!=b and a!=c and a!=d and b!=c and b!=d and c!=d):
							if self.limites(rodas[a], rodas[b], rodas[c], rodas[d]):
								result.append(dict (A=rodas[a], B=rodas[b], C=rodas[c], D=rodas[d], erro=err, razaom=razaom))

		#remove resultados com conjuntos duplicados devido a existirem rodas de muda iguais
		keyfunc = lambda d: (d['A'], d['B'], d['C'], d['D'])
		giter = groupby(sorted(result, key=keyfunc), keyfunc)
		result = [next(g[1]) for g in giter]
		
		#ordena os resultados pelo erro, ascendente
		result = sorted(result, key=itemgetter('erro'))
		
		#limita o numero de resultados a 12
		if len(result) > 12:	
			result = result[0:12]	
		
		return result
		
# Modulo e entradas		
class Heckert (object):
	def __init__ (self, **kwargs) :
		self._name 			= 'Heckert'
		self._modelo 		= 'Heckert ZFWG 250'
		self._conj_rodas	= (20,20,21,22,24,25,27,30,34,35,36,38,40,44,45,46,46,47,48,50,51,52,54,55,56,58,60,62,65,68,70,75,80,85,90,95,100,120,127)	
		self._m 			= kwargs.get('modulo', None)
		self._zO			= kwargs.get('entradas', None)
		if (self._m*pi*self._zO)<=40:
			self._razao = (self._m*self._zO*47)/(6*95)			
		else :
			self._razao = (self._m*self._zO*47)/(40*95)			
			
	def limites(self, *conjunto):
		if len(conjunto) != 4:
			return None
		else :
			A = conjunto[0]
			B = conjunto[1]
			C = conjunto[2]
			D = conjunto[3]

		MIN_AB	=	90			# Original: 78
		MIN_CD	=	90			# Original: 88
		MAX_AB	=	200			# Original: 120
		MAX_CD	=	200			# Original: 135

		if A+B<=MAX_AB and C+D<=MAX_CD and A+B>=MIN_AB  and C+D>=MIN_CD:
			return True
		else :
			return False
			
	def rodasdemuda(self, float erro = 0.001):
		cdef float razaom, err
		razaom = 0
		err = 0
		
		cdef int lrodas, a, b, c, d
		a = 0
		b = 0
		c = 0
		d = 0
		lrodas = len (self._conj_rodas)
		
		cdef vector[float] rodas = self._conj_rodas

		result = []

		for a from 0 <= a < lrodas:
			for b from 0 <= b < lrodas:
				for c from 0 <= c < lrodas:
					for d from 0 <= d < lrodas:
						razaom=rodas[a]/rodas[b]*rodas[c]/rodas[d]
						err = fabs (self._razao - razaom)
						if err<=erro and (a!=b and a!=c and a!=d and b!=c and b!=d and c!=d):
							if self.limites(rodas[a], rodas[b], rodas[c], rodas[d]):
								result.append(dict (A=rodas[a], B=rodas[b], C=rodas[c], D=rodas[d], erro=err, razaom=razaom))

		#remove resultados com conjuntos duplicados devido a existirem rodas de muda iguais
		keyfunc = lambda d: (d['A'], d['B'], d['C'], d['D'])
		giter = groupby(sorted(result, key=keyfunc), keyfunc)
		result = [next(g[1]) for g in giter]
		
		#ordena os resultados pelo erro, ascendente
		result = sorted(result, key=itemgetter('erro'))
		
		#limita o numero de resultados a 12
		if len(result) > 12:	
			result = result[0:12]	
		
		return result
			
# modulo, entradas, modo ou beta
class Spiromatic (object):
	def __init__ (self, **kwargs) :
		self._name 			= 'Spiromatic'
		self._modelo 		= 'Spiromatic'
		self._conj_rodas 	= (31,37,40,41,44,45,47,48,49,50,51,52,53,54,56,57,58,60,61,62,64,66,68,69,72,73,76,78,79,80,80,81,83,89)
		self._w 			= kwargs.get('w', None)
		self._razao 		= self._w

			
	def limites(self, *conjunto):
		if len(conjunto) != 6:
			return None
		else :
			A = conjunto[0]
			B = conjunto[1]
			C = conjunto[2]
			D = conjunto[3]
			E = conjunto[4]
			F = conjunto[5]

		MAX_A	=	80
		MAX_F	=	83
		MIN_AB	=	68
		MIN_EF	=	68
		MAX_AB	=	156
		MAX_EF	=	156

		if A+B>=MIN_AB and E+F>=MIN_EF and A<=MAX_A and F<=MAX_F and A+B<=MAX_AB and E+F<=MAX_EF:
			return True
		else :
			return False
			
	def rodasdemuda(self, float erro = 0.001):
		cdef float razaom, err
		razaom = 0
		err = 0
		
		cdef int lrodas, a, b, e, f
		a = 0
		b = 0
		e = 0
		f = 0
		lrodas = len (self._conj_rodas)
		
		cdef vector[float] rodas = self._conj_rodas

		result = []

		for a from 0 <= a < lrodas:
			for b from 0 <= b < lrodas:
				for e from 0 <= e < lrodas:
					for f from 0 <= f < lrodas:
						razaom=rodas[a]/rodas[b]*rodas[e]/rodas[f]
						err = fabs (self._razao - razaom)
						if err<=erro and (a!=b and a!=e and a!=f and b!=e and b!=f and e!=f):
							if self.limites(rodas[a], rodas[b], 80, 80, rodas[e], rodas[f]):
								result.append(dict (A=rodas[a], B=rodas[b], C=80, D=80, E=rodas[e], F=rodas[f], erro=err, razaom=razaom))

		#remove resultados com conjuntos duplicados devido a existirem rodas de muda iguais
		keyfunc = lambda d: (d['A'], d['B'], d['C'], d['D'], d['E'], d['F'])
		giter = groupby(sorted(result, key=keyfunc), keyfunc)
		result = [next(g[1]) for g in giter]
		
		#ordena os resultados pelo erro, ascendente
		result = sorted(result, key=itemgetter('erro'))
		
		#limita o numero de resultados a 12
		if len(result) > 12:	
			result = result[0:12]	
		
		return result
			
	def rodasdemuda6(self, float erro = 0.001):
		cdef float razaom, err
		razaom = 0
		err = 0
		
		cdef int lrodas, a, b, c, d, e, f
		a = 0
		b = 0
		c = 0
		d = 0
		e = 0
		f = 0
		lrodas = len (self._conj_rodas)
		
		cdef vector[float] rodas = self._conj_rodas

		result = []

		for a from 0 <= a < lrodas:
			for b from 0 <= b < lrodas:
				for c from 0 <= c < lrodas:
					for d from 0 <= d < lrodas:
						for e from 0 <= e < lrodas:
							for f from 0 <= f < lrodas:
								razaom=rodas[a]/rodas[b]*rodas[c]/rodas[d]*rodas[e]/rodas[f]
								err = fabs (self._razao - razaom)
								if err<=erro and (a!=b and a!=c and a!=d and a!=e and a!=f and b!=c and b!=d and b!=e and b!=f and c!=d and c!=e and c!=f and e!=f):
									if self.limites(rodas[a], rodas[b], rodas[c], rodas[d], rodas[e], rodas[f]):
										result.append(dict (A=rodas[a], B=rodas[b], C=rodas[c], D=rodas[d], E=rodas[e], F=rodas[f], erro=err, razaom=razaom))

		#remove resultados com conjuntos duplicados devido a existirem rodas de muda iguais
		keyfunc = lambda d: (d['A'], d['B'], d['C'], d['D'], d['E'], d['F'])
		giter = groupby(sorted(result, key=keyfunc), keyfunc)
		result = [next(g[1]) for g in giter]
		
		#ordena os resultados pelo erro, ascendente
		result = sorted(result, key=itemgetter('erro'))
		
		#limita o numero de resultados a 12
		if len(result) > 12:	
			result = result[0:12]	
		
		return result
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
