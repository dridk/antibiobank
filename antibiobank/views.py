# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from antibiobank.models import *
import json


def index(request):
	context = {'latest_poll_list': 5, 'server':request.META['HTTP_HOST']} 
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

	bactery_id  = request.POST.get("bactery_id",1)
	specimen_id = request.POST.get("specimen_id",1)
	service_id  = request.POST.get("service_id",1)
	filter_mode = request.POST.get("filter_mode", "S")
	filter_ids  = request.POST.getlist("filter_ids[]", None)


	atb = []
	
	records    = Record.objects.filter(bactery_id = bactery_id)
	atbTesting = records.values("resistance__antibiotic__id","resistance__antibiotic__name").distinct()

	if filter_ids != None:
		for id in filter_ids:
			records = records.filter(resistance__antibiotic_id=id, resistance__value=filter_mode)

			


	# records    = records.filter(resistance__antibiotic_id=2, resistance__value="S")
	# records    = records.filter(resistance__antibiotic_id=1, resistance__value="R")

	print "total {}".format(records.count())

	resistances = Resistance.objects.filter(record__in=records)

	for item in atbTesting:
		
		obj = {}
		print item
		obj["name"] = item["resistance__antibiotic__name"]
		obj["id"]   = item["resistance__antibiotic__id"]
		obj["S"] = int(resistances.filter(value="S", antibiotic__id = item["resistance__antibiotic__id"]).count())
		obj["R"] = int(resistances.filter(value="R", antibiotic__id = item["resistance__antibiotic__id"]).count())
		obj["I"] = int(resistances.filter(value="I", antibiotic__id = item["resistance__antibiotic__id"]).count())

		atb.append(obj)

	results = {"name":"Sacha", "data":atb}
	print results



	
	return HttpResponse(json.dumps(results), content_type="application/json")
