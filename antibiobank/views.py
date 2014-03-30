# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg

from antibiobank.models import *
from antibiobank.utils import *
import json
import Image
import pygal


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


	bactery_id   = request.POST.get("bactery_id",1)
	filter_mode  = request.POST.get("filter_mode", "S")
	filter_ids   = request.POST.getlist("filter_ids[]", None)


	results = get_antibio_datas(bactery_id, filter_mode, filter_ids)

	
	return HttpResponse(json.dumps(results), content_type="application/json")



def ajax_image(request):
	


	# results = get_antibio_datas(1,"S")
	# for atb in results["data"]:
	# 	sizes = [atb["S"],atb["I"],atb["R"]]




	# 	i+=1

	pie_chart = pygal.Pie()
	pie_chart.title = 'Browser usage in February 2012 (in %)'
	pie_chart.add('IE', 19.5)
	pie_chart.add('Firefox', 36.6)
	pie_chart.add('Chrome', 36.3)
	pie_chart.add('Safari', 4.5)
	pie_chart.add('Opera', 2.3)


	response = HttpResponse(pie_chart.render(),mimetype="image/svg+xml")
	

	return response
