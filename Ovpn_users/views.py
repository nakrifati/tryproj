from django.shortcuts import render
#from .models import Rule
#from .forms import RuleForm
from datetime import date
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from xml.etree import ElementTree as ET
from django.contrib.auth.decorators import login_required
from os import walk
import os
from os import listdir
from os.path import isfile, join


@login_required
def ovpn_users(request):
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
        only_files = [f for f in listdir("C:/app/openvpn/ccd") if isfile(join("C:/app/openvpn/ccd", f))]

        for FILE in only_files:
            with open('C:/app/openvpn/ccd/' + FILE) as afile:
                data = afile.readline()
                user_ip = data.split()
                print(FILE)
                print(user_ip[1])

    return HttpResponseRedirect('ovpn_users/ovpn_users.html')

