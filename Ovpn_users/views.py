from django.shortcuts import render
from landing.models import Ouser
from landing.forms import OuserForm
from datetime import date
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from xml.etree import ElementTree as ET
from django.contrib.auth.decorators import login_required
from os import listdir
from os.path import isfile, join
from django.db import connection



@login_required
def ovpn_users(request):

    allouser = Ouser.objects.all()
    context = {'allouser': allouser}

    return render(request, 'ovpn_users/ovpn_users.html', locals())


def index(request):
    return render(request, 'home.html', locals())


def create_ovpn_user(request):
    username = request.POST['username']
    out_ip = request.POST['out_ip']

    if request.method == 'POST':
        import os
        my_comd = 'print ' + username + ' ' + out_ip
        print(my_comd)
        os.system(my_comd)

    # return HttpResponse("All done!")
    messages.info(request, 'User Is Added to OpenVPN!')
    return HttpResponseRedirect('ovpn_users/ovpn_users.html')


def list_ovpn_user(request):
    if request.method == 'POST':
        ousers_clear = Ouser.objects.all()
        ousers_clear.delete()
        only_files = [f for f in listdir("C:/app/openvpn/ccd") if isfile(join("C:/app/openvpn/ccd", f))]

        for FILE in only_files:
            with open('C:/app/openvpn/ccd/' + FILE) as afile:
                    data = afile.readline()
                    user_ip = data.split()
                    ip = user_ip[1]
                    print(FILE)
                    print(ip)
                    o_user = Ouser(name=FILE, ip=ip)
                    o_user.save()
                    o_user.clean()
        messages.info(request, 'User Lists is updated!')
                    

    return HttpResponseRedirect('ovpn_users/ovpn_users.html')

