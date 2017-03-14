import sys
import os, os.path
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python\Python36\tcl\tk8.6'

include_files = [os.path.join("acalc", "static"),
				os.path.join("conf"),
				os.path.join("logs")
				]	
				
# packages = [
	# 'distutils', 
	# 'itertools', 
	# 'operator', 
	# 'math', 
	# 'logging', 
	# 'os', 
	# 'cherrypy', 
	# 'cython', 
	# 'jinja2',
	# 'encodings', 
	# 'asyncio'
	# ]				
packages = [
	'itertools', 
	'operator', 
	'math', 
	'logging', 
	'os', 
	'cherrypy', 
	'jinja2',
	'encodings', 
	'asyncio'
	]

includes = None
				
Target = Executable(
			script = "Server.py",
			base = None,
			targetName = "ACalc.exe",
			icon = "acalc\static\images\icon.ico"
			)

setup(  
		name = "ACalc",
		version = "1.1",
		description = "A.Calc application!",
		options = {'build_exe': {
												'includes':includes,
												'packages':packages,
												'include_files':include_files
												}},
		executables = [Target]
		)
