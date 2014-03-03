from django.http import HttpResponse
from django.shortcuts import render


def index(request):
	context = {'latest_poll_list': 5}
	return render(request, "page.html", context)