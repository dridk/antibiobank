#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylab
from antibiobank.models import *
from django.db.models import F
from django.db.models import Q
from django.db.models import Count


def exclusion(records,antibiotic,value):
	toRemove  = records.filter(resistance__antibiotic__name=antibiotic,resistance__value=value)
	return records.exclude(id__in=toRemove)



def create_plot(bactery_id, full_sensibility=None):
	atb = []

	list = ["CEFALOTINE","CEFEPIME"]
	
	records    = Record.objects.filter(bactery_id = bactery_id)
	atbTesting = records.values("resistance__antibiotic__id","resistance__antibiotic__name").distinct()

	records    = records.filter(resistance__antibiotic_id=2, resistance__value="S")
	records    = records.filter(resistance__antibiotic_id=1, resistance__value="R")



	# records    = exclusion(records,"AMOXICILLINE","R")

	# exclusion  = records.filter(resistance__value="S", resistance__antibiotic=1)
	# records    = records.exclude(id__in=exclusion)


 	# records = records.exclude(resistance__antibiotic__name="CEFALOTINE", resistance__value="S")

	print "total {}".format(records.count())

	resistances = Resistance.objects.filter(record__in=records)

	for item in atbTesting:
		
		obj = {}
		print item
		obj["name"] = item["resistance__antibiotic__name"]
		obj["S"] = int(resistances.filter(value="S", antibiotic__id = item["resistance__antibiotic__id"]).count())
		obj["R"] = int(resistances.filter(value="R", antibiotic__id = item["resistance__antibiotic__id"]).count())
		obj["I"] = int(resistances.filter(value="I", antibiotic__id = item["resistance__antibiotic__id"]).count())

		atb.append(obj)

	results = {"name":"Sacha", "data":atb}
	print results

	return results


def run():
	results = create_plot(1)
	print "yes"
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


