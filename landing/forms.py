from django import forms
from .models import *


class SubscribersForm(forms.ModelForm):

    class Meta:
        model = Subscribers1
        exclude = [""]


