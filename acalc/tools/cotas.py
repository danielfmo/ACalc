# -*- coding: utf-8 -*-
__author__	= 'Daniel Oliveira'
__contact__	= 'danielfilipe.mo@gmail.com'
__date__	= '31 March 2013'

from math import sqrt, fabs, sin, cos, tan, ceil, pi, degrees, radians, acos, atan
from .common import six2dec

class Esferas (object):
	def __init__ (self, **kwargs) :
		self._beta 			= kwargs.get('beta', 0)
		self._alfa 			= kwargs.get('alfa', 0)
		self._m 			= kwargs.get('modulo', 0)
		self._a 			= kwargs.get('esfera', 0)
		self._zo 			= kwargs.get('n_dentes', 0)
		self._l 			= kwargs.get('largura', 0)
		self._lb 			= kwargs.get('correcao', 0)
		self._tipo1 		= kwargs.get('tipo1', None)
		self._tipo2			= kwargs.get('tipo2', None)
		
		self._beta 	= radians(six2dec(self._beta))
		self._alfa 	= radians(six2dec(self._alfa))
		
		if self._lb == "":
			self._lb = 0
		else:
		 self._lb = float(self._lb)
		
	def calc_erros (self, D):
		udiv	= 3*self._m+0.04*D+25
		udist	= self._m+0.02*self._l+2
		edist	= 2*udist
		uf		= (0.5+tan(self._alfa))*udiv+edist
		folga	= 2*uf/tan(self._alfa)/1000
		t		= 2*udiv/tan(self._alfa)/1000
		
		calc = dict( udiv	= udiv,
					udist	= udist,
					edist	= edist,
					uf		= uf,
					folga	= folga,
					t		= t
					)
		return calc
		
	def resultado(self):
		if self._a == 0:
			self._a = ceil(self._m*1.75)
		self._P = self._m*pi
		self._S = ( self._m*pi/2 ) + 2*self._lb*self._m*sin(self._alfa)
		self._i=self._P-self._S

		if self._tipo1 == "RECTO":
	
			self._R=self._m*self._zo/2

			self._inv_alfa=(tan(self._alfa)-self._alfa)
			
			if self._tipo2 == "INTERIOR":
				self._inv_teta = self._inv_alfa - self._a/(2*self._R*cos(self._alfa)) + (self._i/(2*self._R)) 
			elif self._tipo2 == "EXTERIOR":
				self._inv_teta = self._inv_alfa + self._a/(2*self._R*cos(self._alfa)) - (self._i/(2*self._R)) 
			
			self._teta_r=0	
			while (tan(self._teta_r)-self._teta_r) < self._inv_teta:
				self._teta_r=self._teta_r+0.000001;
			
			self._L=self._R*cos(self._alfa)/cos(self._teta_r)	#- a no caso de exterior
			
			if(self._zo%2==0):				# PAR
				self._G=2*self._L
			else:							#IMPAR
				self._G=2*self._L*cos( pi/(2*self._zo) )

		if self._tipo1 == "HELICOIDAL":
	
			self._R=self._m*self._zo/(2*cos(self._beta))

			self._cos_ap=cos(self._beta)*cos(self._alfa)
			self.alfa_ap=acos(self._cos_ap)
			
			self._inv_alfa=(tan(self.alfa_ap)-self.alfa_ap)
			
			if self._tipo2 == "INTERIOR":
				self._inv_teta = self._inv_alfa - self._a/(2*self._R*cos(self._alfa)*cos(self._beta)) + (self._i/(2*self._R)) 
			elif self._tipo2 == "EXTERIOR":
				self._inv_teta = self._inv_alfa + self._a/(2*self._R*cos(self._alfa)*cos(self._beta)) - (self._i/(2*self._R)) 
			
			self._teta_r=0	
			while (tan(self._teta_r)-self._teta_r) < self._inv_teta:
				self._teta_r=self._teta_r+0.000001;
			
			self._L=self._R*cos(self.alfa_ap)/cos(self._teta_r)
			
			if(self._zo%2==0):				# PAR
				self._G=2*self._L
			else:							#IMPAR
				self._G=2*self._L*cos( pi/(2*self._zo) )				
		
		self._teta_r 	= degrees(self._teta_r)
		
		resultado = {}
		resultado['a'] 			= self._a
		resultado['R'] 			= self._R
		resultado['inv_teta'] 	= self._inv_teta
		resultado['teta'] 		= self._teta_r
		resultado['erro'] 		= self.calc_erros(2*self._R)
		resultado['G'] 			= self._G-resultado['erro']['folga']
		
		return resultado
	
class EkEngrenagem (object):
	def __init__ (self, **kwargs) :
		self._beta 			= str(kwargs.get('beta', 0))
		self._alfa 			= str(kwargs.get('alfa', 0))
		self._m 			= kwargs.get('modulo', None)
		self._z1 			= kwargs.get('n_dentes1', None)
		self._l				= kwargs.get('largura', None)
		self._dp			= kwargs.get('dp', 0)
		self._dentes_ek1	= kwargs.get('dentes_ek1', None)
		self._tipo1 		= kwargs.get('tipo1', None)
		self._tipo2			= kwargs.get('tipo2', None)
		
		if self._tipo1 == "HELICOIDAL":
			self._beta 	= radians(six2dec(self._beta))
		elif self._tipo1 == "RECTO":
			self._beta 	= 0
		self._alfa 	= radians(six2dec(self._alfa))
		if self._dp == 0:
			self._dp = self._m*self._z1/cos(self._beta)
			
	def calc_ek (self, z0, dentes):
		EX	= self._m*cos(self._alfa)
		ES	= (dentes-0.5)*pi
		EL	= (z0*self._inv_alfa)	
		EK	= EX*(ES+EL)
		return EK	
		
	def calc_m (self, z0, dentes, ek):
		ES	= (dentes-0.5)*pi
		EL	= (z0*self._inv_alfa)
		EX	= ek/(ES+EL)
		M	= EX/cos(self._alfa)
		return M
	
	def calc_erros (self, D):
		udiv	= (3*self._map+0.04*D+25)*cos(self._beta)
		udist	= (self._map+0.02*self._l+2)*cos(self._beta)
		edist	= 2*udist
		uf		= (0.5+tan(self._alfaap))*udiv+edist
		folga	= 2*uf*cos(self._alfaap)/1000
		t		= udiv*cos(self._alfaap)/1000

		calc = dict( udiv	= udiv,
					udist	= udist,
					edist	= edist,
					uf		= uf,
					folga	= folga,
					t		= t
					)
		return calc
	
	def resultado(self):
		
		self._zi			= self._z1/(cos(self._beta)*cos(self._beta)*cos(self._beta))
		
		if self._dentes_ek1 == 0:
			self._dentes_ek1	= ceil(self._z1*(self._alfa/pi))

		self._map		= self._m/cos(self._beta)
		self._alfaap 	= atan(tan(self._alfa) / cos(self._beta))
		self._inv_alfa	= tan(self._alfaap)-self._alfaap

		self._EE		= self._m*self._z1/cos(self._beta)
		
		self._D1		= self._EE
		
		self._carreto	= {}
		self._roda		= {}
		resultado		= {}

		# Se DENTRO do entre-eixo de funcionamento
		if self._EE == self._dp:
			self._carreto['erro']	= self.calc_erros(self._D1)
			self._carreto['erro']['fc']	= 0
			self._carreto['de'] 	= self._D1+2*self._m
			self._carreto['EK'] 	= self.calc_ek(self._z1, self._dentes_ek1)-self._carreto['erro']['folga']	
			
		# Se FORA do entre-eixo de funcionamento			
		else:
			self._z2 = self._z1
			
			self._K		= self._EE*cos(self._alfaap)/self._dp
			self._K1	= pi*0.5-atan(self._K/sqrt(-self._K*self._K+1)) 
			self._W1	= (self._z1+self._z2)/(2*tan(self._alfa))
			self._inv_k1= tan(self._K1)-self._K1
			self._W2	= self._inv_k1-self._inv_alfa
			self._W		= self._W1*self._W2
			self._B		= 2*self._W/(self._z1+self._z2)
			self._BV	= cos(self._alfaap)/cos(self._K1)-1
			self._K2	= (self._B-self._BV/cos(self._beta))*(self._z1+self._z2)/2

			self._zv1=self._zi
			self._zv2=self._zi

			self._carreto['E'] 		= self.calc_ek(self._z1, self._dentes_ek1)
			self._carreto['erro']	= self.calc_erros(self._D1)	

			self._DELTA1	=(self._W*self._zv1)/(self._z2+self._zv1)
			
			self._carreto['EK']		= self._carreto['E']-self._carreto['erro']['folga']+(2*self._DELTA1*self._m*sin(self._alfa))
			self._carreto['erro']['fc']	= self._DELTA1	
			self._carreto['de'] 	= self._m*(self._z1/cos(self._beta)+2+(2*self._DELTA1)-(2*self._K2))
			
		self._carreto['dentes_ek1'] = self._dentes_ek1

		resultado['carreto']	= self._carreto
		resultado['dp']			= self._dp
		if self._tipo2 =="ESQUERDA":
			resultado['carreto']['sentido'] = "Esquerda"
		if self._tipo2 =="DIREITA":
			resultado['carreto']['sentido'] = "Direita"
			
		return resultado
			
class EkConjunto (object):
	def __init__ (self, **kwargs) :
		self._beta 			= str(kwargs.get('beta', 0))
		self._alfa 			= str(kwargs.get('alfa', 0))
		self._m 			= kwargs.get('modulo', None)
		self._z1 			= kwargs.get('n_dentes1', None)
		self._z2 			= kwargs.get('n_dentes2', None)
		self._l				= kwargs.get('largura', None)
		self._eef			= kwargs.get('eef', 0)
		self._dentes_ek1	= kwargs.get('dentes_ek1', None)
		self._dentes_ek2	= kwargs.get('dentes_ek2', None)
		self._tipo1 		= kwargs.get('tipo1', None)
		self._tipo2			= kwargs.get('tipo2', None)
		self._fixek1		= kwargs.get('ek1_fix', None)
		self._ek1			= kwargs.get('ek1', None)
		self._fixek2		= kwargs.get('ek2_fix', None)
		self._ek2			= kwargs.get('ek2', None)
		
		if self._tipo1 == "RECTO":
			self._beta 	= 0

		if self._ek1 != None:
			self._ek1 = float(self._ek1)
		if self._ek2 != None:
			self._ek2 = float(self._ek2)
			
		if self._tipo1 == "HELICOIDAL":
			self._beta 	= radians(six2dec(self._beta))
			
		self._alfa 	= radians(six2dec(self._alfa))

		if self._eef == 0:
			self._eef = self._m*(self._z1+self._z2)/(2*cos(self._beta))
		
	def calc_ek (self, z0, dentes):
		EX	= self._m*cos(self._alfa)
		ES	= (dentes-0.5)*pi
		EL	= (z0*self._inv_alfa)	
		EK	= EX*(ES+EL)
		return EK	
		
	def calc_m (self, z0, dentes, ek):
		ES	= (dentes-0.5)*pi
		EL	= (z0*self._inv_alfa)
		EX	= ek/(ES+EL)
		M	= EX/cos(self._alfa)
		return M
	
	def calc_erros (self, D):
		udiv	= (3*self._map+0.04*D+25)*cos(self._beta)
		udist	= (self._map+0.02*self._l+2)*cos(self._beta)
		edist	= 2*udist
		uf		= (0.5+tan(self._alfaap))*udiv+edist
		folga	= 2*uf*cos(self._alfaap)/1000
		t		= udiv*cos(self._alfaap)/1000

		calc = dict( udiv	= udiv,
					udist	= udist,
					edist	= edist,
					uf		= uf,
					folga	= folga,
					t		= t
					)
		return calc
	
	def resultado(self):
		if self._dentes_ek1 == 0:
			self._dentes_ek1 = ceil(self._z1*(self._alfa/pi))
		if self._dentes_ek2 == 0:
			self._dentes_ek2 = ceil(self._z2*(self._alfa/pi))

		self._map		= self._m/cos(self._beta)
		self._alfaap 	= atan(tan(self._alfa) / cos(self._beta))
		self._inv_alfa	= tan(self._alfaap)-self._alfaap

		self._EE		= self._m*(self._z1+self._z2)/(2*cos(self._beta))
		
		self._D1		= self._m*self._z1/cos(self._beta)
		self._D2		= self._m*self._z2/cos(self._beta)
		
		#self._EE		= (self._D1+self._D2)/2
		
		self._carreto	= {}
		self._roda		= {}
		resultado		= {}

		# Se DENTRO do entre-eixo de funcionamento
		if self._EE == self._eef:
			# Calculo normal
			if self._fixek1 == None and self._fixek2 == None :
				self._carreto['EK'] = self.calc_ek(self._z1, self._dentes_ek1)
				self._roda['EK'] 	= self.calc_ek(self._z2, self._dentes_ek2)
			
			# calcular EK1 com EK2 fixo
			elif self._fixek1 == None and self._fixek2 == "ON":
				self._m 			= self.calc_m(self._z2, self._dentes_ek2, self._ek2)
				self._carreto['EK'] = self.calc_ek(self._z1, self._dentes_ek1)
				self._roda['EK'] 	= self._ek2
				
			# calcular EK2 com EK1 fixo
			elif self._fixek1 == "ON" and self._fixek2 == None :
				self._m 			= self.calc_m(self._z1, self._dentes_ek1, self._ek1)
				self._carreto['EK'] = self._ek1
				self._roda['EK'] 	= self.calc_ek(self._z2, self._dentes_ek2)
				
			self._D1		= self._m*self._z1/cos(self._beta)
			self._D2		= self._m*self._z2/cos(self._beta)			
			
			self._carreto['erro']	= self.calc_erros(self._D1)
			self._roda['erro'] 		= self.calc_erros(self._D2)
			self._carreto['de'] 	= 2*self._m+self._D1
			self._roda['de'] 		= 2*self._m+self._D2
			self._carreto['erro']['fc']	= 0	
			self._roda['erro']['fc']	= 0
		if self._fixek1 == None:
			self._carreto['EK'] = self._carreto['EK']-self._carreto['erro']['folga']
		if self._fixek2 == None:
			self._roda['EK'] 	= self._roda['EK']-self._roda['erro']['folga']
			
			
		# Se FORA do entre-eixo de funcionamento			
		else:
			self._K		= self._EE*cos(self._alfaap)/self._eef
			self._K1	= pi*0.5-atan(self._K/sqrt(-self._K*self._K+1)) 
			self._W1	= (self._z1+self._z2)/(2*tan(self._alfa))
			self._inv_k1= tan(self._K1)-self._K1
			self._W2	= self._inv_k1-self._inv_alfa
			self._W		= self._W1*self._W2
			self._B		= 2*self._W/(self._z1+self._z2)
			self._BV	= cos(self._alfaap)/cos(self._K1)-1
			self._K2	= (self._B-self._BV/cos(self._beta))*(self._z1+self._z2)/2

			self._zv1=self._z1/( cos(self._beta)*cos(self._beta)*cos(self._beta) )
			self._zv2=self._z2/( cos(self._beta)*cos(self._beta)*cos(self._beta) )
			
			self._carreto['E'] 		= self.calc_ek(self._z1, self._dentes_ek1)
			self._roda['E'] 		= self.calc_ek(self._z2, self._dentes_ek2)
			self._carreto['erro']	= self.calc_erros(self._D1)	
			self._roda['erro'] 		= self.calc_erros(self._D2)
			
			# Calculo normal
			if self._fixek1 == None and self._fixek2 == None :
				self._DELTA1	= 0.5*(self._zv2-self._zv1)/(self._zv2+self._zv1)+(self._W*self._zv1)/(self._z2+self._zv1)
				self._DELTA2	= self._W-self._DELTA1

				self._carreto['EK']		= self._carreto['E']-self._carreto['erro']['folga']+(2*self._DELTA1*self._m*sin(self._alfa))
				self._roda['EK']		= self._roda['E']-self._roda['erro']['folga']+(2*self._DELTA2*self._m*sin(self._alfa))
								
			# calcular EK1 com EK2 fixo
			elif self._fixek1 == None and self._fixek2 == "ON":
				self._DELTA2		= (self._ek2-self._roda['E']+self._roda['erro']['folga'])/(2*self._m*sin(self._alfa))
				self._DELTA1		= self._W - self._DELTA2;
				self._roda['EK'] 	= self._ek2
				self._carreto['EK'] = self._carreto['E']-self._carreto['erro']['folga']+(2*self._DELTA1*self._m*sin(self._alfa))
								
			# calcular EK2 com EK1 fixo
			elif self._fixek1 == "ON" and self._fixek2 == None :
				self._DELTA1		= (self._ek1-self._carreto['E']+self._carreto['erro']['folga'])/(2*self._m*sin(self._alfa))
				self._DELTA2		= self._W - self._DELTA1;
				self._carreto['EK'] = self._ek1
				self._roda['EK'] 	= self._roda['E']-self._roda['erro']['folga']+(2*self._DELTA2*self._m*sin(self._alfa))
						
			
			self._carreto['erro']['fc']	= self._DELTA1	
			self._roda['erro']['fc']	= self._DELTA2
		
			self._carreto['de'] 	= self._m*(self._z1/cos(self._beta)+2+(2*self._DELTA1)-(2*self._K2))
			self._roda['de'] 		= self._m*(self._z2/cos(self._beta)+2+(2*self._DELTA2)-(2*self._K2))		
			
		self._carreto['dentes_ek'] = self._dentes_ek1
		self._roda['dentes_ek'] 	= self._dentes_ek2

		resultado['carreto']	= self._carreto
		resultado['roda']		= self._roda
		resultado['eef']		= self._eef
		
		if self._tipo2 =="ESQUERDA":
			resultado['carreto']['sentido'] = "Esquerda"
			resultado['roda']['sentido'] = "Direita"	
		if self._tipo2 =="DIREITA":
			resultado['carreto']['sentido'] = "Direita"
			resultado['roda']['sentido'] = "Esquerda"
			
		return resultado

class EkSemfim (object):
	def __init__ (self, **kwargs) :
		self._beta 			= kwargs.get('beta', 0)
		self._alfa 			= str(kwargs.get('alfa', 0))
		self._m 			= kwargs.get('modulo', None)
		self._z1 			= kwargs.get('n_dentes1', None)
		self._z2 			= kwargs.get('n_dentes2', None)
		self._l				= kwargs.get('largura', None)
		self._eef			= kwargs.get('eef', None)
		self._dentes_ek1	= kwargs.get('dentes_ek1', None)
		self._dentes_ek2	= kwargs.get('dentes_ek2', None)
		self._sentido 		= kwargs.get('sentido', None)
		self._fixM			= kwargs.get('M_fix', None)
		self._fixG			= kwargs.get('G_fix', None)
		self._M				= kwargs.get('M', None)
		self._G				= kwargs.get('G', None)
		self._a				= kwargs.get('esfera', None)

		if self._M != None:
			self._M = float(self._M)
		if self._G != None:
			self._G = float(self._G)
			
		self._alfa 	= radians(six2dec(self._alfa))
		
	def calc_cotasM (self):
		a	= self._PN/self._z1/2-2*self._m*1.25*tan(self._alfa)
		b	= self._PN/self._z1/2+2*self._m*tan(self._alfa)
		c	= self._PN/self._z1-b
		d	= self._m*1.25
		e	= self._m
		f	= self._m*2.25
		dp	= self._D1
		cota = dict ( 	a = a,
						b = b,
						c = c,
						d = d,
						e = e,
						f = f,
						dp = dp)
		return cota				
	
	def calc_cotasG (self):
		a	= self._D1/2+self._m*1.25
		b	= self._D1/2
		c	= self._D1/2-self._m
		d	= self._D2+self._m*3
		e	= self._D2+self._m*2
		f	= None
		dp	= self._D2
		cota = dict ( 	a = a,
						b = b,
						c = c,
						d = d,
						e = e,
						f = f,
						dp = dp)		
		return cota
		
	def calc_erros (self, D):
		udiv	= 3*self._m+0.04*D+25
		udist	= self._m+0.02*self._l+2
		edist	= 2*udist
		uf		= (0.5+tan(self._alfa))*udiv+edist
		folga	= 4*uf/tan(self._alfa)/1000
		t		= 2*udiv/tan(self._alfa)/1000

		calc = dict( udiv	= udiv,
					udist	= udist,
					edist	= edist,
					uf		= uf,
					folga	= folga,
					t		= t
					)
		return calc
	
	def calc_M (self):
		self._PAX		= self._m*self._z1*pi
		self._PN		= self._PAX*cos(self._beta)
		self._EE		= self._m*pi/2
		self._M2		= self._D1 - ( (self._PN/self._z1/2)/tan(self._alfa) ) + self._a*(1/sin(self._alfa)-1)

		if self._z1%2 != 0:
			self._M		= sqrt( pow((self._M2+self._a),2)+pow(self._EE,2) )-self._a
		else:
			self._M 	= self._M2	
	
	def calc_G (self):
		self._AX1		= -1*self._EE + ( self._a/(cos(self._alfaap)*cos(self._betaap)) )
		self._AX2		= self._D2*self._inv_alfa
		self._inv_teta	= (self._AX1+self._AX2)/self._D2
			
		self._teta=0	
		while (tan(self._teta)-self._teta) < self._inv_teta:
			self._teta=self._teta+0.000001;
			
		self._L=self._D2*cos(self._alfaap)/cos(self._teta)
		
		if(self._z2%2==0):	
			self._G=self._L-self._a
		else:	
			self._G=self._L*cos( pi/(2*self._z2) )-self._a	
	
	
	def resultado(self):
		if self._a == 0:
			self._a = ceil(self._m*1.75)
			
		self._beta 	= radians(six2dec(self._beta))
		
		self._semfim	= {}
		self._roda		= {}
		resultado		= {}

		# Calculo normal
		if self._fixM == None and self._fixG == None :
			self._D2		= self._m*self._z2
			self._D1		= (self._eef-self._D2/2)*2
			
			if self._beta == 0:
				self._beta = atan(self._m*self._z1/self._D1)
				
			self._alfaap 	= atan(tan(self._alfa) / cos(self._beta))
			self._inv_alfa	= tan(self._alfaap)-self._alfaap	
			self._betaap 	= atan(tan(self._beta) * cos(self._alfaap))
			
			# Calculo de M
			self.calc_M()
			# Calculo de G
			self.calc_G()
			

		elif self._fixM == None and self._fixG == "ON" :
			self._alfaap 	= atan(tan(self._alfa) / cos(self._beta))
			self._inv_alfa	= tan(self._alfaap)-self._alfaap	
			self._betaap 	= atan(tan(self._beta) * cos(self._alfaap))

			# Calculo de G
			self._teta=pi/2
			self._Gt = 0
			while self._Gt < self._G:
				self._teta=self._teta-0.000001;
				self._inv_teta = tan(self._teta)-self._teta
				self._D2 = (2*self._a-self._m*pi*cos(self._betaap)*cos(self._alfaap))/( 2*cos(self._betaap)*cos(self._alfaap)*(self._inv_teta-self._inv_alfa))
				
				self._L=self._D2/2*cos(self._alfaap)/cos(self._teta)
				
				if self._z2%2==0 :	
					self._Gt=self._L*2-self._a
				else:	
					self._Gt=self._L*cos( pi/(2*self._z2) )*2-self._a	
			self._D1	= (self._eef-self._D2/2)*2
			# Calculo de M
			self.calc_M()	
			
		elif self._fixM == "ON" and self._fixG == None :
			self._alfaap 	= atan(tan(self._alfa) / cos(self._beta))
			self._inv_alfa	= tan(self._alfaap)-self._alfaap	
			self._betaap 	= atan(tan(self._beta) * cos(self._alfaap))

			# Calculo de M
			self._PAX		= self._m*self._z1*pi
			self._PN		= self._PAX*cos(self._beta)
			self._EE		= self._m*pi/2

			if self._z1%2 != 0:
				self._M2 = sqrt( pow((self._M+self._a),2)+pow(self._EE,2) )-self._a
				self._D1 = self._M2 + ( ((self._PN/self._z1)/2)/tan(self._alfa) ) - self._a*(1/sin(self._alfa)-1)
			else:
				self._D1 = self._M  + ( ((self._PN/self._z1)/2)/tan(self._alfa) ) - self._a*(1/sin(self._alfa)-1)
			
			self._D2	 = (self._eef-self._D1/2)*2
			# Calculo de G
			self.calc_G()			
		
		self._semfim['M']	= self._M
		self._semfim['erro']= self.calc_erros(self._D1)
		self._semfim['cotas'] = self.calc_cotasM()
		self._roda['G']		= self._G
		self._roda['erro']	= self.calc_erros(self._D2)		
		self._roda['cotas']	= self.calc_cotasG()
		
		if self._fixM == None:
			self._semfim['M']	= self._M-self._semfim['erro']['folga']
		if self._fixG == None:
			self._roda['G']		= self._G-self._roda['erro']['folga']
		
		if self._sentido =="ESQUERDA":
			self._semfim['sentido'] = "Esquerda"
			self._roda['sentido']	= "Esquerda"	
		elif self._sentido =="DIREITA":
			self._semfim['sentido'] = "Direita"
			self._roda['sentido']	= "Direita"
			
		resultado['semfim']	= self._semfim
		resultado['roda']	= self._roda
		resultado['a']		= self._a
		resultado['beta']	= degrees(self._beta)
	
		return resultado
		
		
		
		
		
		
		