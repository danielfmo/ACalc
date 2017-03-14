from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("rodasdemuda", ["rodasdemuda.pyx"], language='c++' )]

setup(
  name = 'ACalc',
  version = '0.1',
  description = 'test library', 
  author = "Daniel Oliveira", 
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
