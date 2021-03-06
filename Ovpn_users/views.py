from django.shortcuts import render
from landing.models import Ouser
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from os import listdir
from os.path import isfile, join
import telnetlib
from landing.models import OnlineUser
from time import gmtime, strftime
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from landing.models import Rule
from xml.etree import ElementTree as ET


CCD_address = 'C:/app/openvpn/ccd/'


@login_required
def ovpn_users(request):

    allouser = Ouser.objects.all()
    all_online = OnlineUser.objects.all()
    context = {'allouser': allouser}
    paginator = Paginator(allouser, 25)  # Show 20 contacts per page.

    page_number = request.GET.get('page')
    allouser = paginator.get_page(page_number)
    result = -1

    HOST = "localhost"
    QUESTION = "status 3"
    try:
        tn = telnetlib.Telnet(HOST, 7505)

    except ConnectionRefusedError:
        messages.info(request, '([WinError 10061] Подключение не установлено, т.к. конечный компьютер отверг '
                               'запрос на подключение), another exception occurred')
        result = -1
    else:
        tn.read_until(b"OpenVPN Management Interface")
        tn.write(QUESTION.encode('ascii') + b"\n")

        tn.write(b"ls\n")
        tn.write(b"exit\n")

        users = tn.read_all().decode('ascii')
        print(users, file=open('temp.txt', "w"))

        result = users.count('CLIENT_LIST') - 1

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

    import os

    try:
        count_users = len(next(os.walk('/etc/openvpn/ccd/'))[2])
    except StopIteration:
        total_users = 0

    else:
        total_users = count_users

    total_online = result
    fh.close()

    return render(request, 'ovpn_users/ovpn_users.html', locals())


def index(request):
    return render(request, 'home.html', locals())


def create_ovpn_user(request):
    username = request.POST['username']

    if request.method == 'POST':

        if request.POST.get('out_all', False):
            out_ip = '0.0.0.0/0'
            print(out_ip)
        else:
            out_ip = request.POST['out_ip']
            print(out_ip)

        import os
        my_comd = './new-vpn-user-auto.sh ' + username + ' ' + out_ip
        print(my_comd + ' ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()), file=open("log.txt", "a"))
        os.system(my_comd)

    messages.info(request, 'User Is Added to OpenVPN!')

    root = ET.parse('templates/testdata/direct.xml').getroot()

    rules = Rule.objects.all()
    rules.delete()

    for type_tag in root.iter('rule'):
        table = type_tag.get('table')
        ipv = type_tag.get('ipv')
        chain = type_tag.get('chain')
        priority = type_tag.get('priority')
        print(type_tag.text)
        p = Rule(priority=priority, table=table, ipv=ipv, chain=chain, rule_value=type_tag.text)
        p.save()
        p.clean()

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
                    o_user = Ouser(name=FILE, ip=ip)
                    o_user.save()
                    o_user.clean()
        messages.info(request, 'User Lists is updated!')

    return HttpResponseRedirect('ovpn_users/ovpn_users.html')


def revoke_ovpn_user(request):
    username_r = request.POST['username_r']

    if request.method == 'POST':
        import os
        revoke_cmd = 'openssl ca -config /usr/easyrsa3/pki/safessl-easyrsa.cnf -revoke /etc/openvpn/keys/' + \
                     username_r + '.crt ' + ' -batch -key passwd'
        print(revoke_cmd + ' ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()), file=open("log.txt", "a"))
        os.system(revoke_cmd)

    messages.info(request, 'User is successfully revoked!')

    return HttpResponseRedirect('ovpn_users/ovpn_users.html')


def user_list(request):
    posts_list = Ouser.objects.all()
    query = request.GET.get('q')
    if query:
        posts_list = Ouser.objects.filter(
            Q(name__icontains=query) | Q(ip__icontains=query)
        ).distinct()

    context = {
        'posts': posts_list
    }
    
    return render(request, "ovpn_users/ovpn_users.html", context, locals())
