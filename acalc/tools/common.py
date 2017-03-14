# -*- coding: utf-8 -*-
__author__    = 'Daniel Oliveira'
__contact__   = 'danielfilipe.mo@gmail.com'
__date__      = '31 March 2013'

import os
import logging

from jinja2 import Environment, FileSystemLoader
jinja_env = Environment(loader=FileSystemLoader(os.path.join("acalc", "static", "templates")))

log = logging.getLogger(__name__)

def render_template(template, **kwargs):
	return jinja_env.get_template(template).render(**kwargs)
    
def six2dec(angle):
	import re
	pat = r"^(\d+)[º ](\d+)[' ]([\d.]*)['']?"
	angle_dec = 0 
	r = re.compile(pat)
	angle_match = r.match(angle)

	if angle_match is None:
		angle_dec = float(angle)
	else:
		grau, minuto, segundo = angle_match.groups()
		angle_dec = float(grau) + float(minuto)/60 + float(segundo)/3600
	
	return angle_dec;