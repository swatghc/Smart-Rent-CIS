from django.shortcuts import render
from django.views import generic
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from .models import Property, Agency, Resource
from .realestate_crawler import real_estate_crawler
from django.views.decorators import csrf
from .models import Property,Agency,Resource

# Create your views here.
def indexView(request):
    template_name = "webapp/index.html"
    return render(request,template_name)

def getData(request):
    print('hahahha')
    data = real_estate_crawler.gather_information(1, 'melbourne')
    page = data[0]
    agent_name = page['agent']
    agent_img = page['agentPic']
    house_type = page['houseType']
    original_link = page['urlDetail']
    house_img = page['housePic']
    price = page['price']
    location = page['location']
    bed = page['bed']
    bath = page['bathroom']
    showDataTemplate='webapp/showData.html'
    return render(request, showDataTemplate, {'page': page, 'agent_name': agent_name, 'agent_img': agent_img, 'house_type': house_type,
                                              'original_link': original_link, 'house_img': house_img, 'price': price,
                                              'location': location, 'bed': bed, 'bath': bath})


def search_basic(request):
    if request.POST:
        searhInput = request.POST['basic-input']
        print('--------------')
        print(searhInput)
        print('--------------')

        searchResultTemplate='webapp/searchBasic1.html'

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
    crawled_info = real_estate_crawler.gather_information(1, 'melbourne')
    size = len(crawled_info)
    pList = []
    aList = []
    rList = []
    for i in range(0, size):
        feature = crawled_info[i]
        pList.append(Property())
        aList.append(Agency())
        rList.append(Resource())
        pList[i].address = feature['location']
        pList[i].house_img = feature['housePic']
        pList[i].loc_rating = 5
        pList[i].fac_rating = 5
        pList[i].tran_rating = 5
        pList[i].comment = 'good'
        pList[i].no_bed = feature['bed']
        pList[i].no_bath = feature['bathroom']
        pList[i].house_type = feature['houseType']
        pList[i].save()

        aList[i].name = feature['agentPeople']
        aList[i].agent_img = feature['agentPic']
        aList[i].company = feature['agentCompany']
        aList[i].company_logo = 'https://www.siasat.com/wp-content/uploads/2017/11/real-estate.jpg'
        aList[i].fri_rating = 5
        aList[i].res_rating = 5
        aList[i].bond_rating = 5
        aList[i].comment = 'good'
        aList[i].save()

        rList[i].property = pList[i]
        rList[i].agency = aList[i]
        rList[i].link = feature['urlDetail']
        rList[i].price = feature['price']
        rList[i].save()
        print(rList[i])
        print('r is saved')

    showResultTemplate = 'webapp/showResult.html'
    return render(request, showResultTemplate, {'crawled_info':crawled_info})

def queryTable(request):
    rr = Resource.objects.filter(price__lt=500)
    print(rr)
    # rr_filtered = rr.values()
    # print(rr_filtered)
    # for eachrr in rr:
    #     eachpp = eachrr.property_set.all()
    #     print(eachpp)
    # ppReady = pp.filter(address__contains='1').filter(no_bed__contains='2')
    # print(ppReady)
    showQuery = 'webapp/showQuery.html'
    return render(request, showQuery)


def aboutView(request):
    return render(request,'webapp/about.html')

def detailView(request,property_id):
    resource = get_object_or_404(Resource,pk=property_id)
    return render(request,'webapp/detail.html',{'resource':resource})




