from django.shortcuts import render
from .models import Rule
from .forms import SubscribersForm
from datetime import date
from django.shortcuts import redirect
from xml.etree import ElementTree as ET
root = ET.parse('templates/testdata/direct.xml').getroot()


def landing(request):

    form = SubscribersForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(request.POST)
#       print(form.cleaned_data)
        save_form = form.save()

    today = date.today()


    return render(request, 'landing/landing.html', locals())


def index(request):

    return render(request, 'index.html', locals())


def action_url(request):
    if request.method('action_url'):
        ar = []
        ar.clear()
        for type_tag in root.iter('rule'):
            priority = type_tag.get('priority')
            table = type_tag.get('table')
            ipv = type_tag.get('ipv')
            chain = type_tag.get('chain')
            ar.append(type_tag.text)
            print(type_tag.text)
            p = Rule(priority=priority, table=table, ipv=ipv, chain=chain, rule_value=type_tag.text)
            p.save()
            return redirect('landing/landing.html')

        allrules = Rule.objects.all()
        context = {'allrules': allrules}

    return render(request, 'landing/landing.html', locals())


