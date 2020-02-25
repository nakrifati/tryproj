from django.conf.urls import url, include
from django.contrib import admin
from ovpn_users import views
from django.urls import path


urlpatterns = [

    url(r'ovpn_users/', views.ovpn_users, name='ovpn_users'),
    url(r'create_ovpn_user', views.create_ovpn_user, name='create_ovpn_user'),
    url(r'list_ovpn_user', views.list_ovpn_user, name='list_ovpn_user'),
    url(r'revoke_ovpn_user', views.revoke_ovpn_user, name='revoke_ovpn_user'),

]

