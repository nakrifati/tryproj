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

CCD_address = 'C:/app/openvpn/ccd/'


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
        my_comd = './new-vpn-user-auto.sh ' + username + ' ' + out_ip
        print(my_comd, file=open("log.txt", "a"))
        os.system(my_comd)

    # return HttpResponse("All done!")
    messages.info(request, 'User Is Added to OpenVPN!')
    return list_ovpn_user(request)


def list_ovpn_user(request):
    if request.method == 'POST':
        ousers_clear = Ouser.objects.all()
        ousers_clear.delete()
        only_files = [f for f in listdir(CCD_address) if isfile(join(CCD_address, f))]

        for FILE in only_files:
            with open(CCD_address + FILE) as afile:
                    data = afile.readline()
                    user_ip = data.split()
                    ip = user_ip[1]
                    print(FILE, file=open("log.txt", "a"))
                    print(ip, file=open("log.txt", "a"))
                    o_user = Ouser(name=FILE, ip=ip)
                    o_user.save()
                    o_user.clean()
        messages.info(request, 'User Lists is updated!')

    return HttpResponseRedirect('ovpn_users/ovpn_users.html')

