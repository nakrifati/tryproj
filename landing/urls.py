from django.conf.urls import url, include
from django.contrib import admin
from landing import views
from django.urls import path


urlpatterns = [

    url(r'landing/', views.landing, name='landing'),
    url(r'action_url', views.action_url, name='action_url'),
    url(r'export_to_xml', views.export_to_xml, name='export_to_xml'),
    url(r'non', views.index, name='index'),

]

