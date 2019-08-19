from django.contrib import admin
from .models import *


# class SubscriberAdmin (admin.ModelAdmin):
#     list_display = [field.name for field in Subscriber._meta.fields]
#     list_filter = ["name"]
#     search_fields = ["name"]
#
#     class Meta:
#         model = Subscriber


class RuleAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Rule._meta.fields]

    class Meta:
        model = Rule


class OuserAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Ouser._meta.fields]

    class Meta:
        model = Ouser


#admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Ouser, OuserAdmin)
