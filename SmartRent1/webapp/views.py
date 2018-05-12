from django.shortcuts import render
from django.views import generic
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
#from .models import Property
from realestate_crawler import real_estate_crawler
# Create your views here.
def indexView(request):
    template_name = "webapp/index.html"
    return render(request,template_name)

#def getProperty(request):


def saveToTable(request) :
    propertyInLine = real_estate_crawler.gather_information(1)
    print(propertyInLine)
    size = len(propertyInline)
    pList = [None]*size
    # pList is the list of properties in the format of objects. the objects have the attributes such as address and rulDetail

    for i in range(0, size-1):
        propertyItem = propertyInLine[i]
        pList.append(Property())
        pList[i].urlDetail = propertyItem['urlDetail']
        pList[i].address = propertyItem['location']
        #Don't forget houseType
        pList[i].save()

    return pList
