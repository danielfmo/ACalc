# -*- coding: utf-8 -*-
__author__ = 'Daniel Oliveira'
__contact__ = 'danielfilipe.mo@gmail.com'
__date__ = '31 March 2013'


import cherrypy
from acalc.tools.common import render_template
from acalc.tools.calculos import CalcSpiro


class SpiroPage:
    @cherrypy.expose
    def index(self):
        return render_template("calc_spiromatic.html", resultado=[])

    @cherrypy.expose
    def passo1(self, **kwargs):
        self._sentido = str(kwargs.get('radio1', None)).upper()
        self._m = float(kwargs.get('modulo', None))
        self._z1 = float(kwargs.get('z1', None))
        self._z2 = float(kwargs.get('z2', None))
        self._e = float(kwargs.get('e', None))
        self._alfa = float(kwargs.get('alfa', None))

        self = CalcSpiro().passo1(kwargs=kwargs)

        return render_template("calc_spiromatic.html",
                               resultado=self,
                               values=None)


class CalcPage:
    def __init__(self):
        self.spiromatic = SpiroPage()

    @cherrypy.expose
    def index(self):
        return render_template("calc.html")
