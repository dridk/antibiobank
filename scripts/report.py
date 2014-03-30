#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylab
from antibiobank.models import *
from antibiobank.utils import *
from django.db.models import F
from django.db.models import Q
from django.db.models import Count

def run():
	results = get_antibio_datas(1)
	print "yes"
	col  = 4
	row  = (len(results["data"])/col) + 1

	fig = pylab.Figure(facecolor="red")
	fig.set_axis_on()
	# fig.canvas.set_window_title(results["name"])
	colors = ["#77DD77","#FFB347","#FF6961"]
	i=1
	for atb in results["data"]:
		sizes = [atb["S"],atb["I"],atb["R"]]
		pylab.subplot(row,col,i)
		pylab.title(atb["name"], fontsize=10)
		pylab.pie(sizes, colors=colors)
		pylab.axis('equal')
		i+=1

	pylab.subplots_adjust(hspace = .5)
	pylab.axis('equal')
	pylab.show()


