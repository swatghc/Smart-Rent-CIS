from django.shortcuts import render
from django.views import generic
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
#from .models import Property
#from realestate_crawler import real_estate_crawler
# Create your views here.
def indexView(request):
    template_name = "webapp/index.html"
    return render(request,template_name)

#def getProperty(request):


