# -*- coding: utf-8 -*-
__author__    = 'Daniel Oliveira'
__contact__   = 'danielfilipe.mo@gmail.com'
__date__      = '31 March 2013'

import os
import logging

from jinja2 import Environment, FileSystemLoader

if os.path.isdir("/home/danielfmo/ACalc/acalc/static/templates"):
	template_path = os.path.join("/home/danielfmo/ACalc/acalc/static/templates")
else :
	template_path = os.path.join("acalc", "static", "templates")
	
jinja_env = Environment(loader=FileSystemLoader(template_path))

log = logging.getLogger(__name__)

def render_template(template, **kwargs):
	return jinja_env.get_template(template).render(**kwargs)
    
def six2dec(angle):
	import re
	pat = r"^(\d+)[\s](\d+)[\s]([\d.]*)[\s]?"
	angle_dec = 0 
	r = re.compile(pat)
	angle_match = r.match(angle)

	if angle_match is None:
		angle_dec = float(angle)
	else:
		grau, minuto, segundo = angle_match.groups()
		angle_dec = float(grau) + float(minuto)/60 + float(segundo)/3600
	
	return angle_dec;	