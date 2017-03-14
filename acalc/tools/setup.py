from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

extensions = [Extension("rodasdemuda", ["rodasdemuda.pyx"], language='c++' )]

#extensions = cythonize(extensions)

setup(
  name = 'rodasDeMuda',
  version = '1.1',
  description = 'test library', 
  author = "Daniel Oliveira", 
  cmdclass = {'build_ext': build_ext},
  ext_modules = extensions
)
