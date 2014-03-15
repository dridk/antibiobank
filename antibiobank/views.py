# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from antibiobank.models import *
import json


def index(request):
	context = {'latest_poll_list': 5}
	return render(request, "page.html", context)

def ajax_bacteries(request):
	response_data = []	
	for b in Bactery.objects.all():
		response_data.append({"id": b.id, "name":unicode(b)})
	return HttpResponse(json.dumps({"results":response_data}), content_type="application/json")

def ajax_services(request):
	response_data = []
	for b in Service.objects.all():
		response_data.append({"id": b.id, "name":unicode(b)})
	return HttpResponse(json.dumps({"results":response_data}), content_type="application/json")

def ajax_specimens(request):
	response_data = []
	for b in Specimen.objects.all():
		response_data.append({"id": b.id, "name":unicode(b)})
	return HttpResponse(json.dumps({"results":response_data}), content_type="application/json")

def ajax_stats(request):

	print request.POST

	bactery_id  = request.POST["bactery_id"]
	specimen_id = request.POST["bactery_id"]
	service_id  = request.POST["bactery_id"]


	# service = request.POST["service"]
	# specimen = request.POST["specimen"]



	atb = []
	resistances = Resistance.objects.filter(record__bactery_id = bactery_id)


	print resistances.count()


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


	return HttpResponse(json.dumps(atb), content_type="application/json")
