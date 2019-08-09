from django.shortcuts import render
from .models import Rule
from .forms import RuleForm
from datetime import date
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from xml.etree import ElementTree as ET

root = ET.parse('templates/testdata/direct.xml').getroot()



def landing(request):

    form = RuleForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(request.POST)
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

        for type_tag in root.iter('rule'):
            table = type_tag.get('table')
            ipv = type_tag.get('ipv')
            chain = type_tag.get('chain')
            priority = type_tag.get('priority')
            # ar.append(type_tag.text)
            print(type_tag.text)
            p = Rule(priority=priority, table=table, ipv=ipv, chain=chain, rule_value=type_tag.text)
            p.save()

    return redirect('landing/')


def export_to_xml(request):
    if request.method == 'POST':

        allrules = Rule.objects.all()
        """
            Создаем XML файл.
            
            """
        root = ET.Element("direct")

        for rule in allrules:
            rule_xml = ET.Element("rule")
            root.append(rule_xml)
            rule_xml.set("priority", rule.priority)
            rule_xml.set("chain", rule.chain)
            rule_xml.set("ipv", rule.ipv)
            rule_xml.set("table", rule.table)
            rule_xml.text = rule.rule_value

        open('templates/testdata/catalogs.xml', 'w').close()
        print(ET.tostring(root, encoding='utf8', method='xml').decode(), file=open("templates/testdata/catalogs.xml", "a"))

        """replace string"""

        f = open('templates/testdata/catalogs.xml', 'r')
        filedata = f.read()
        f.close()

        newdata = filedata.replace("utf8", "utf-8")

        f = open('templates/testdata/catalogs.xml', 'w')
        f.write(newdata)
        f.close()

        #return HttpResponse("All done!")
        messages.info(request, 'Rules have been exported!')
        return HttpResponseRedirect('landing/')


