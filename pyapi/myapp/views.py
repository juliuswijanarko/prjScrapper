from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def get_tr(request, user, pss):
	if request.method == 'GET':
		return HttpResponse('Hello', content_type='text/json')