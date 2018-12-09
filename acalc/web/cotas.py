# -*- coding: utf-8 -*-
__author__ = 'Daniel Oliveira'
__contact__ = 'danielfilipe.mo@gmail.com'
__date__ = '31 March 2013'


import cherrypy
import logging
from acalc.tools.common import render_template
from acalc.tools.cotas import Esferas, EkEngrenagem, EkConjunto, EkSemfim


class EsferasPage:
    @cherrypy.expose
    def index(self):
        return render_template("cotas_esferas.html")

    @cherrypy.expose
    def result(self, **kwargs):
        self._artigo = str(kwargs.get('artigo', ""))
        self._beta = str(kwargs.get('beta', 0))
        self._alfa = str(kwargs.get('alfa', 0))
        self._m = float(kwargs.get('modulo', 0))
        self._a = int(kwargs.get('esfera', 0))
        self._zo = int(kwargs.get('n_dentes', 0))
        self._l = float(kwargs.get('largura', 0))
        self._lb = kwargs.get('correcao', None)
        self._tipo1 = str(kwargs.get('radio1', None)).upper()
        self._tipo2 = str(kwargs.get('radio2', None)).upper()

        self._result = []
        self._message = ""
        self._values = ""

        try:
            self._result = Esferas(	beta=self._beta,
                                    alfa=self._alfa,
                                    modulo=self._m,
                                    esfera=self._a,
                                    n_dentes=self._zo,
                                    largura=self._l,
                                    correcao=self._lb,
                                    tipo1=self._tipo1,
                                    tipo2=self._tipo2
                                    ).resultado()

            self._values = "<strong>Artigo:</strong> {} [n] [n]".format(
                self._artigo)
            self._values = self._values + \
                "<strong>Tipo do dentado:</strong> {}  {} [n]".format(
                    self._tipo1, self._tipo2)
            self._values = self._values + \
                "<strong>Ângulo de Pressão:</strong> {} [n]".format(self._alfa)
            if self._beta != "0":
                self._values = self._values + \
                    "<strong>Ângulo da Hélice:</strong> {}[n]".format(
                        self._beta)
            self._values = self._values + \
                "<strong>Módulo:</strong> {} mm [n]<strong>N. de dentes:</strong> {} ".format(
                    self._m, self._zo)
            self._values = self._values + \
                "[n]<strong>Largura do dentado:</strong> {}".format(self._l)

            self._a = self._result['a']

        except:
            self._message = "Não é possivel concluir o cálculo com os valores introduzidos"
            self._carreto = None
            cherrypy.log(msg=self._message, context='',
                         severity=logging.ERROR, traceback=True)

        return render_template("cotas_esferas.html",
                               beta=self._beta,
                               alfa=self._alfa,
                               modulo=self._m,
                               esfera=self._a,
                               n_dentes=self._zo,
                               largura=self._l,
                               correcao=self._lb,
                               result=self._result,
                               artigo=self._artigo,
                               message=self._message,
                               values=self._values)


class EkEngrPage:
    @cherrypy.expose
    def index(self):
        return render_template("cotas_ek_engrenagem.html")

    @cherrypy.expose
    def result(self, **kwargs):
        self._artigo = str(kwargs.get('artigo', ""))
        self._beta = str(kwargs.get('beta', 0))
        self._alfa = str(kwargs.get('alfa', 0))
        self._m = float(kwargs.get('modulo', 0))
        self._z1 = int(kwargs.get('n_dentes1', 0))
        self._l = float(kwargs.get('largura', 0))
        self._dp = float(kwargs.get('eef', 0))
        self._dentes_ek1 = int(kwargs.get('dentes_ek1', 0))
        self._tipo1 = str(kwargs.get('radio1', None)).upper()
        self._tipo2 = str(kwargs.get('radio2', None)).upper()

        self._result = []
        self._message = ""
        self._values = ""

        try:
            self._result = EkEngrenagem(	beta=self._beta,
                                         alfa=self._alfa,
                                         modulo=self._m,
                                         n_dentes1=self._z1,
                                         largura=self._l,
                                         dp=self._dp,
                                         dentes_ek1=self._dentes_ek1,
                                         tipo1=self._tipo1,
                                         tipo2=self._tipo2
                                         ).resultado()

            self._dentes_ek1 = self._result['carreto']['dentes_ek1']
            self._carreto = self._result['carreto']
            self._dp = self._result['dp']
            self._values = "<strong>Artigo:</strong> {} [n] [n]".format(
                self._artigo)
            self._values = self._values + \
                "<strong>Tipo do dentado:</strong> {} [n]<strong>Ângulo de Pressão:</strong> {} [n]".format(
                    self._tipo1, self._alfa)
            if self._beta != "0":
                self._values = self._values + \
                    "<strong>Ângulo da Hélice:</strong> {}[n]".format(
                        self._beta)
            self._values = self._values + \
                "[n]<strong>Módulo:</strong> {} mm [n]<strong>Largura do dentado:</strong> {} [n]<strong>Diâmetro Primitivo:</strong> {} ".format(
                    self._m, self._l, self._dp)
            self._values = self._values + \
                "[n]<strong>N. Dentes:</strong> {}".format(self._z1)

        except:
            self._message = "Não é possivel concluir o cálculo com os valores introduzidos"
            self._carreto = None
            cherrypy.log(msg=self._message, context='',
                         severity=logging.ERROR, traceback=True)

        return render_template("cotas_ek_engrenagem.html",
                               beta=self._beta,
                               alfa=self._alfa,
                               modulo=self._m,
                               n_dentes1=self._z1,
                               largura=self._l,
                               dp=self._dp,
                               dentes_ek1=self._dentes_ek1,
                               tipo1=self._tipo1,
                               tipo2=self._tipo2,
                               carreto=self._carreto,
                               artigo=self._artigo,
                               message=self._message,
                               values=self._values)


class EkConjPage:
    @cherrypy.expose
    def index(self):
        return render_template("cotas_ek_conjunto.html")

    @cherrypy.expose
    def result(self, **kwargs):
        self._artigo = str(kwargs.get('artigo', ""))
        self._beta = str(kwargs.get('beta', 0))
        self._alfa = str(kwargs.get('alfa', 0))
        self._m = float(kwargs.get('modulo', 0))
        self._z1 = int(kwargs.get('n_dentes1', 0))
        self._z2 = int(kwargs.get('n_dentes2', 0))
        self._eef = float(kwargs.get('eef', 0))
        self._l = float(kwargs.get('largura', 0))
        self._dentes_ek1 = int(kwargs.get('dentes_ek1', 0))
        self._dentes_ek2 = int(kwargs.get('dentes_ek2', 0))
        self._tipo1 = str(kwargs.get('radio1', None)).upper()
        self._tipo2 = str(kwargs.get('radio2', None)).upper()
        self._fixek1 = kwargs.get('ek1_fix', None)
        self._fixek2 = kwargs.get('ek2_fix', None)
        self._ek1 = kwargs.get('ek1', None)
        self._ek2 = kwargs.get('ek2', None)

        self._result = []
        self._message = ""
        self._values = ""

        try:
            self._result = EkConjunto(	beta=self._beta,
                                       alfa=self._alfa,
                                       modulo=self._m,
                                       n_dentes1=self._z1,
                                       n_dentes2=self._z2,
                                       largura=self._l,
                                       eef=self._eef,
                                       dentes_ek1=self._dentes_ek1,
                                       dentes_ek2=self._dentes_ek2,
                                       ek1_fix=self._fixek1,
                                       ek1=self._ek1,
                                       ek2_fix=self._fixek2,
                                       ek2=self._ek2,
                                       tipo1=self._tipo1,
                                       tipo2=self._tipo2).resultado()

            self._dentes_ek1 = self._result['carreto']['dentes_ek']
            self._dentes_ek2 = self._result['roda']['dentes_ek']
            self._carreto = self._result['carreto']
            self._roda = self._result['roda']
            self._eef = self._result['eef']

            self._values = "<strong>Artigo:</strong> {} [n] [n]".format(
                self._artigo)
            self._values = self._values + \
                "<strong>Tipo do dentado:</strong> {} [n]<strong>Ângulo de Pressão:</strong> {}".format(
                    self._tipo1, self._alfa)
            if self._beta != "0":
                self._values = self._values + \
                    "[n]<strong>Ângulo da Hélice:</strong> {}".format(
                        self._beta)
            self._values = self._values + \
                "[n]<strong>Módulo:</strong> {} mm [n]<strong>Largura do dentado:</strong> {} [n]<strong>Entre-eixo de funcionamento:</strong> {} ".format(
                    self._m, self._l, self._eef)
            self._values = self._values + \
                "[n]<strong>N. Dentes CARRETO:</strong> {} [n]<strong>N. Dentes RODA:</strong> {}".format(
                    self._z1, self._z2)

        except:
            self._message = "Não é possivel concluir o cálculo com os valores introduzidos"
            self._carreto = None
            self._roda = None
            cherrypy.log(msg=self._message, context='',
                         severity=logging.ERROR, traceback=True)

        return render_template("cotas_ek_conjunto.html",
                               beta=self._beta,
                               alfa=self._alfa,
                               modulo=self._m,
                               n_dentes1=self._z1,
                               n_dentes2=self._z2,
                               largura=self._l,
                               eef=self._eef,
                               dentes_ek1=self._dentes_ek1,
                               dentes_ek2=self._dentes_ek2,
                               tipo1=self._tipo1,
                               tipo2=self._tipo2,
                               carreto=self._carreto,
                               roda=self._roda,
                               artigo=self._artigo,
                               message=self._message,
                               values=self._values)


class EkSemfimPage:
    @cherrypy.expose
    def index(self):
        return render_template("cotas_semfim.html")

    @cherrypy.expose
    def result(self, **kwargs):
        self._artigo = str(kwargs.get('artigo', ""))
        self._beta = str(kwargs.get('betas', 0))
        self._alfa = str(kwargs.get('alfa', 0))
        self._m = float(kwargs.get('modulo', 0))
        self._z1 = int(kwargs.get('n_dentes1', 0))
        self._z2 = int(kwargs.get('n_dentes2', 0))
        self._l = float(kwargs.get('largura', 0))
        self._eef = float(kwargs.get('eef', 0))
        self._a = int(kwargs.get('esfera', 0))
        self._sentido = str(kwargs.get('radio1', None)).upper()
        self._fixM = kwargs.get('ek1_fix', None)
        self._fixG = kwargs.get('ek2_fix', None)
        self._M = kwargs.get('ek1', None)
        self._G = kwargs.get('ek2', None)

        self._result = []
        self._message = ""
        self._values = ""

        try:
            self._result = EkSemfim(	beta=self._beta,
                                     alfa=self._alfa,
                                     modulo=self._m,
                                     n_dentes1=self._z1,
                                     n_dentes2=self._z2,
                                     largura=self._l,
                                     eef=self._eef,
                                     esfera=self._a,
                                     sentido=self._sentido,
                                     M_fix=self._fixM,
                                     G_fix=self._fixG,
                                     M=self._M,
                                     G=self._G
                                     ).resultado()

            self._a = self._result['a']
            self._beta = self._result['beta']
            self._semfim = self._result['semfim']
            self._roda = self._result['roda']

            self._values = "<strong>Artigo:</strong> {} [n] [n]".format(
                self._artigo)
            self._values = self._values + \
                "<strong>Sentido da Hélice:</strong> {} [n]".format(
                    self._sentido)
            self._values = self._values + \
                "<strong>Ângulo de Pressão:</strong> {} [n]".format(self._alfa)
            self._values = self._values + \
                "<strong>Ângulo da Hélice:</strong> {}  [n]".format(self._beta)
            self._values = self._values + \
                "<strong>Módulo Axial:</strong> {} mm [n]".format(self._m)
            self._values = self._values + \
                "<strong>N. entradas do SEM-FIM:</strong> {} [n]".format(
                    self._z1)
            self._values = self._values + \
                "<strong>N. dentes do RODA:</strong> {} ".format(self._z2)

        except:
            self._message = "Não é possivel concluir o cálculo com os valores introduzidos"
            self._semfim = None
            self._roda = None
            cherrypy.log(msg=self._message, context='',
                         severity=logging.ERROR, traceback=True)

        return render_template("cotas_semfim.html",
                               beta=self._beta,
                               alfa=self._alfa,
                               modulo=self._m,
                               n_dentes1=self._z1,
                               n_dentes2=self._z2,
                               largura=self._l,
                               eef=self._eef,
                               esfera=self._a,
                               semfim=self._semfim,
                               roda=self._roda,
                               artigo=self._artigo,
                               message=self._message,
                               values=self._values)


class CotasPage:
    def __init__(self):
        self.esferas = EsferasPage()
        self.ek_engrenagem = EkEngrPage()
        self.ek_conjunto = EkConjPage()
        self.ek_semfim = EkSemfimPage()

    @cherrypy.expose
    def index(self):
        return render_template("cotas.html")
