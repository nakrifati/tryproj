from django.shortcuts import render
from .models import Rule
from .forms import RuleForm
from datetime import date
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core import serializers
from django.core.files import File
from xml.etree import ElementTree as ET
from xml.dom import minidom
import os

root = ET.parse('templates/testdata/direct.xml').getroot()


def landing(request):

    form = RuleForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(request.POST)
#       print(form.cleaned_data)
        save_form = form.save()

    today = date.today()

    allrules = Rule.objects.all()
    context = {'allrules': allrules}

    return render(request, 'landing/landing.html', locals())


def index(request):

    return render(request, 'index.html', locals())


def action_url(request):
    if request.method == "POST":
        print(request.POST)
        rules = Rule.objects.all()
        rules.delete()
        # ar = []
        # ar.clear()
        for type_tag in root.iter('rule'):
            priority = type_tag.get('priority')
            table = type_tag.get('table')
            ipv = type_tag.get('ipv')
            chain = type_tag.get('chain')
            # ar.append(type_tag.text)
            print(type_tag.text)
            p = Rule(priority=priority, table=table, ipv=ipv, chain=chain, rule_value=type_tag.text)
            p.save()

    return redirect('landing/')


def export_to_xml(request):
    if request.method == 'POST':
        #data = serializers.serialize("xml", Rule.objects.all())
        #f = open('templates/testdata/catalogs.xml', 'w')
        #myfile = File(f)
        #myfile.write('<?xml version="1.0" encoding="utf-8"?>')
        #for i in range(10):
        #    myfile.write("This is line %d\r\n" % (i + 1))
        #myfile.close()

        #filename = open('templates/testdata/catalogs.xml', 'w')
        # output = ET.Element("Users")
        # userelement = ET.Element("user")
        # output.append(userelement)
        # with open(filename, "w") as fh:
        #     output.write(fh)

        """
            Создаем XML файл.
            """
        root = ET.Element("direct")
        rule_xml = ET.Element("rule")
        root.append(rule_xml)

        # создаем дочерний суб-элемент.
        rule_xml.set("priority", "0")
        rule_xml.set("table", "nat")
        rule_xml.set("ipv", "ipv4")
        rule_xml.set("chain", "POSTROUTING")
        rule_xml.text = "o tun1 -j MASQUERADE d"

        open('templates/testdata/catalogs.xml', 'w').close()
        print(ET.tostring(root, encoding='utf8', method='xml').decode(), file=open("templates/testdata/catalogs.xml", "a"))

        #tree = ET.ElementTree(root)

        #tree.write('templates/testdata/catalogs.xml')

        return HttpResponse("All done!")

