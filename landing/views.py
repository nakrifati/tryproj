from django.shortcuts import render
from datetime import date
from xml.etree import ElementTree as ET
tree = ET.parse('templates/testdata/direct.xml')
root = tree.getroot()
from .forms import SubscribersForm



def landing(request):
    for xmlout in root.findall('.direct'):
        print(xmlout.find('rule').text)

    form = SubscribersForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(request.POST)
#       print(form.cleaned_data)
        save_form = form.save()

    today = date.today()


    return render(request, 'landing/landing.html', locals())


def index(request):


    return render(request, 'index.html', locals())


