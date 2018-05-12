from django.conf.urls import url
from . import views
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static


app_name = 'webapp'

urlpatterns = [
    path('index/',views.indexView,name='index'),
    path('search-basic/',views.search_basic, name='basicSearch'),
    path('search-advanced/',views.search_advanced, name='advancedSearch'),

]