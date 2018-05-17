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

def search_basic(request):
    if request.POST:
        searhInput = request.POST['basic-input']
        print('--------------')
        print(searhInput)
        print('--------------')

        result_basic = Resource.objects.filter(property__address__contains=str(searhInput)).select_related('property').select_related('agency')
        # result_basic = result_basic.distinct(result_basic,result_basic.property.address)
        # for each in result_basic:
        #     print(each.price + '   ' + str(each.property.no_bed))

        searchResultTemplate = 'webapp/searchBasic.html'
        return render(request, searchResultTemplate, {'result_basic': result_basic})

def search_advanced(request):
    if request.POST:
        advanced_input = {
            'uniName': request.POST['uni-name'],
            'houseType': request.POST['house-type'],
            'maxPrice': request.POST['max-price'],
            'bedNum': request.POST['bed-num']
        }

        result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).select_related('property').filter(property__house_type__exact=advanced_input['houseType']).filter(
            property__no_bed__exact=advanced_input['bedNum']).select_related('agency')
        # result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).select_related('property').filter(
        #     propertyproperty__no_bed__exact=advanced_input['bedNum']).select_related('agency')
        print(result_advanced)
        for each in result_advanced:
            print(each.price + '   ' + str(each.property.no_bed)+'   ' + str(each.property.house_type))

        print('***************')
        print(advanced_input)
        print('***************')
        searchResultTemplate = 'webapp/searchAdvanced.html'
        # return render(request,searchResultTemplate,{'advanced_input':advanced_input})
        return render(request, searchResultTemplate, {'result_advanced': result_advanced})

def saveToTable(request) :
    crawled_info = real_estate_crawler.gather_information(10, 'melbourne')
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

def aboutView(request):
    return render(request,'webapp/about.html')

def detailView(request,id):
    resource = get_object_or_404(Resource,pk=id)
    return render(request,'webapp/detail.html',{'resource':resource})





