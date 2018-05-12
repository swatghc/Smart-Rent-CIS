from django.shortcuts import render
from django.views import generic
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from .models import Property
from .realestate_crawler import real_estate_crawler
from django.views.decorators import csrf

# Create your views here.
def indexView(request):
    template_name = "webapp/index.html"
    return render(request,template_name)

def getData(request):
    print('hahahha')
    data = real_estate_crawler.gather_information(1)
    page = data[0]
    agent_img=page['agentPic']
    print(agent_img)
    house_type = page['houseType']
    print(house_type)
    showDataTemplate='webapp/showData.html'
    return render(request, showDataTemplate, {'page': page, 'agent_img': agent_img, 'house_type': house_type})


def search_basic(request):
    if request.POST:
        searhInput = request.POST['basic-input']
        print('--------------')
        print(searhInput)
        print('--------------')

        searchResultTemplate='webapp/searchBasic.html'

        return render(request,searchResultTemplate,{'searhInput':searhInput})

def search_advanced(request):
    if request.POST:
        advanced_input = {
            'uniName': request.POST['uni-name'],
            'houseType': request.POST['house-type'],
            'maxPrice': request.POST['max-price'],
            'bedNum': request.POST['bed-num']
        }
        print('***************')
        print(advanced_input)
        print('***************')
        searchResultTemplate = 'webapp/searchAdvanced.html'
        return render(request,searchResultTemplate,{'advanced_input':advanced_input})

def saveToTable(request) :
    propertyInLine = real_estate_crawler.gather_information(1)
    print(propertyInLine)
    size = len(propertyInLine)
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
