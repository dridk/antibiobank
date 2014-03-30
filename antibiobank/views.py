# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg

from antibiobank.models import *
from antibiobank.utils import *
import json
import Image
import pylab


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
	


	results = get_antibio_datas(1,"S")

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

	canvas = FigureCanvasAgg(fig)   
	response = HttpResponse(mimetype="image/png")
	canvas.print_png(response)

	return response
