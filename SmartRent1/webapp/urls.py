from django.conf.urls import url
from . import views
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static


app_name = 'webapp'

urlpatterns = [
    path('index/',views.indexView,name='index'),
    path('showData/',views.getProperty,name='showData'),


]