from django.shortcuts import render
from .models import Rule
from .forms import RuleForm
from datetime import date
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from xml.etree import ElementTree as ET
from django.contrib.auth.decorators import login_required
import os
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q

root = ET.parse('templates/testdata/direct.xml').getroot()
target_xml = 'templates/testdata/catalogs.xml'


@login_required
def landing(request):

    form = RuleForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.rule_value = request.POST['rule_value']
        print(request.POST)
        save_form = form.save()

    today = date.today()

    allrules = Rule.objects.all()
    context = {'allrules': allrules}
    paginator = Paginator(allrules, 30)  # Show 20 contacts per page.

    page_number = request.GET.get('page')
    allrules = paginator.get_page(page_number)

    return render(request, 'landing/landing.html', locals())


def index(request):

    return render(request, 'home.html', locals())


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
            print(type_tag.text)
            p = Rule(priority=priority, table=table, ipv=ipv, chain=chain, rule_value=type_tag.text)
            p.save()
            p.clean()

    return redirect('landing/')


def export_to_xml(request):
    if request.method == 'POST':

        allrules = Rule.objects.all()
        """  Создаем XML файл.  """

        root = ET.Element("direct")

        for rule in allrules:
            rule_xml = ET.Element("rule")
            root.append(rule_xml)
            rule_xml.set("chain", rule.chain)
            rule_xml.set("ipv", rule.ipv)
            rule_xml.set("table", rule.table)
            rule_xml.set("priority", rule.priority)
            rule_xml.text = rule.rule_value

        open(target_xml, 'w').close()
        print(ET.tostring(root, encoding='utf8', method='xml').decode(), file=open(target_xml, "a"))

        """replace strings"""

        f = open(target_xml, 'r')
        filedata = f.read()
        f.close()

        newdata = filedata.replace("utf8", "utf-8")
        newdata2 = newdata.replace("</rule>", "</rule> \n")
        newdata3 = newdata2.replace("t>", "t> \n")

        f = open(target_xml, 'w')
        f.write(newdata3)
        f.close()

        my_cmd = 'firewall-cmd --reload'
        os.system(my_cmd)

        messages.info(request, 'Rules have been exported!')
        return HttpResponseRedirect('landing/')


def post_list(request):
    posts_list = Rule.objects.all()
    query = request.GET.get('q')
    if query:
        posts_list = Rule.objects.filter(
            Q(rule_value__icontains=query)
        ).distinct()

    context = {
        'posts': posts_list
    }
    return render(request, "landing/landing.html", context, locals())

