from django.shortcuts import render
from datetime import date
from .forms import SubscribersForm


def landing(request):
    form = SubscribersForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(request.POST)
#       print(form.cleaned_data)
        save_form = form.save()

    today = date.today()
    return render(request, 'landing/landing.html', locals())
