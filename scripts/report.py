#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylab
from antibiobank.models import *


def create_plot(bactery_id):
	atb = []
	resistances = Resistance.objects.filter(record__bactery_id = bactery_id)


	for item in resistances.values_list("antibiotic__name", "antibiotic__id").distinct():
		s_value = 40
		r_value = 50
		i_value = 10

		obj = {}
		obj["name"] = item[0]
		obj["S"] = int(resistances.filter(value="S", antibiotic__id = item[1]).count())
		obj["R"] = int(resistances.filter(value="R", antibiotic__id = item[1]).count())
		obj["I"] = int(resistances.filter(value="I", antibiotic__id = item[1]).count())

		atb.append(obj)
	print atb
	return atb


def run():
	data = create_plot(1)
	col  = 4
	row  = (len(data)/col) + 1


	colors = ["#77DD77","#FFB347","#FF6961"]
	i=1
	for atb in data:
		sizes = [atb["S"],atb["I"],atb["R"]]
		pylab.subplot(row,col,i)

		pylab.title(atb["name"], fontsize=10)
		pylab.pie(sizes, colors=colors)
		pylab.axis('equal')



		i+=1

	pylab.subplots_adjust(hspace = .5)
	pylab.axis('equal')
	pylab.show()


