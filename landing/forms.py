from django import forms
from .models import *


class SubscribersForm(forms.ModelForm):

    class Meta:
        model = Subscriber
        exclude = [""]


class RuleForm(forms.ModelForm):

    class Meta:
        model = Rule
        exclude = [""]


