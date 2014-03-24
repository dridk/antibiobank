#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylab
from antibiobank.models import *
from django.db.models import F
from django.db.models import Q


def create_plot(bactery_id, full_sensibility=None):
	atb = []

	list = ["CEFALOTINE","CEFEPIME"]
	

	q = Q(**{"resistance__antibiotic__name":"CEFALOTINE"})
	q = q and Q(**{"resistance__antibiotic__name":"CEFEPIME"})




	records = Record.objects.filter(bactery_id = bactery_id)

	records = records.filter(q, resistance__value="R")



	print records.count()

	# resistances = Resistance.objects.filter(record__bactery_id = bactery_id)
	# resistances = resistances.filter(antibiotic__name="CEFEPIME", value="S")
	bacterie = Bactery.objects.filter(pk=bactery_id)

	resistances = Resistance.objects.filter(record__in=records)
	items = resistances.values_list("antibiotic__name", "antibiotic__id")


	for item in items.distinct():
		s_value = 40
		r_value = 50
		i_value = 10

		obj = {}
		obj["name"] = item[0]
		obj["S"] = int(resistances.filter(value="S", antibiotic__id = item[1]).count())
		obj["R"] = int(resistances.filter(value="R", antibiotic__id = item[1]).count())
		obj["I"] = int(resistances.filter(value="I", antibiotic__id = item[1]).count())

		atb.append(obj)

	results = {"name":str(bacterie), "data":atb}

	return results


def run():
	results = create_plot(2)
	col  = 4
	row  = (len(results["data"])/col) + 1

	fig = pylab.gcf()
	fig.canvas.set_window_title(results["name"])
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


