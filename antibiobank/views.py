# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from antibiobank.models import *
import json


def index(request):
	context = {'latest_poll_list': 5}
	return render(request, "page.html", context)

def ajax_bacteries(request):
	response_data = []	for b in Bactery.objects.all():
		response_data.append(unicode(b))
	return HttpResponse(json.dumps({"results":response_data}), content_type="application/json")

def ajax_services(request):
	response_data = []
	for b in Service.objects.all():
		response_data.append(unicode(b))
	return HttpResponse(json.dumps({"results":response_data}), content_type="application/json")

def ajax_specimens(request):
	response_data = []
	for b in Specimen.objects.all():
		response_data.append(unicode(b))

	return HttpResponse(json.dumps({"results":response_data}), content_type="application/json")

def ajax_stats(request):
		if request.method == "GET":
			print "get params : " + str(request.GET)

		if request.method == "POST":
			print "post params : "+ str(request.POST)

		print "type of "

		atb = []
		resistances = Resistance.objects.filter(record__bactery_id=1)
		
		for item in resistances.values_list("antibiotic__name").distinct():
			s_value = 40
			r_value = 50
			i_value = 10

			obj = {}
			obj["name"] = item[0]
			obj["S"] = int(resistances.filter(value="S", antibiotic__name = item[0]).count())
			obj["R"] = int(resistances.filter(value="R", antibiotic__name = item[0]).count())
			obj["I"] = int(resistances.filter(value="I", antibiotic__name = item[0]).count())

			atb.append(obj)



		return HttpResponse(json.dumps(atb), content_type="application/json")
