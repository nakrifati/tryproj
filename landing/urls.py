from django.conf.urls import url, include
from django.contrib import admin
from landing import views
from django.urls import path


urlpatterns = [

    url(r'landing/', views.landing, name='landing'),
    url(r'landing/', views.action_url),
    url(r'', views.index, name='index'),

]

