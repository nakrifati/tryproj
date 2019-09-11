from django.shortcuts import render
from landing.models import Ouser
from landing.forms import OuserForm
from datetime import date
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from os import listdir
from os.path import isfile, join
import telnetlib
from sys import argv
import array as arr
from landing.models import OnlineUser


CCD_address = 'C:/app/openvpn/ccd/'


@login_required
def ovpn_users(request):

    allouser = Ouser.objects.all()
    all_online = OnlineUser.objects.all()
    context = {'allouser': allouser}

    # HOST = "localhost"
    # QUESTION = "status 3"
    # tn = telnetlib.Telnet(HOST, 7505)
    #
    # tn.read_until(b"OpenVPN Management Interface")
    # tn.write(QUESTION.encode('ascii') + b"\n")
    #
    # tn.write(b"ls\n")
    # tn.write(b"exit\n")
    #
    # users = tn.read_all().decode('ascii')
    # print(users, file=open('temp.txt', "w"))
    #
    # result = users.count('CLIENT_LIST') - 1
    result = -1
    if result < 0:
        result = 0

    users_online = []

    fh = open('temp.txt')
    clear_db_online = OnlineUser.objects.all()
    clear_db_online.delete()

    for line in fh:
        if "CLIENT_LIST" in line:
            if "HEADER" not in line:
                login = line.split()[1]
                r_ip = line.split()[2]
                v_ip = line.split()[3]
                online_since = ' '.join(line.split()[6:10])
                save_online = OnlineUser(login=login, r_ip=r_ip, v_ip=v_ip, online_since=online_since)
                save_online.save()
                save_online.clean()

    total_online = result

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



