import sys
import os, os.path
from cx_Freeze import setup, Executable

include_files = [os.path.join("acalc", "static"),
				os.path.join("conf"),
				os.path.join("logs")
				]

packages = [
	"distutils", 
	"itertools", 
	"operator", 
	"math", 
	"logging", 
	"os", 
	"cherrypy", 
	"cython", 
	"jinja2"]

includes = None
				
Target = Executable(
			script = "Server.py",
			base = None,
			targetName = "ACalc.exe",
			compress = True,
			copyDependentFiles = True,
			icon = "acalc\static\images\icon.ico"
			)

setup(  name = "ACalc",
		version = "0.1",
		description = "A.Calc application!",
		options = {'build_exe': {'includes':includes,'packages':packages,'include_files':include_files}},
		executables = [Target])
