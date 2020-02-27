from django.db import models
from django.views.generic import ListView

Chain_choices = (
    ('FORWARD','FORWARD'),
    ('POSTROUTING', 'POSTROUTING'),
)

ipv_choices = (
    ('ipv4','ipv4'),
)

table_choices = (
    ('filter','filter'),
    ('nat', 'nat'),
)

priority_choices = (
    ('0','0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
)

# class Subscriber(models.Model):
#     email = models.EmailField(blank=True)
#     name = models.CharField(max_length=128, blank=True)
#
#     def __str__(self):
#         return "%s %s %s" % (self.name, self.email, self.id)


class Rule(models.Model):
    priority = models.CharField(max_length=256, choices=priority_choices, default='0')
    table = models.CharField(max_length=256, choices=table_choices, default='filter')
    ipv = models.CharField(max_length=64, choices=ipv_choices, default='ipv4')
    chain = models.CharField(max_length=256, choices=Chain_choices, default='FORWARD')
    rule_value = models.CharField(max_length=256, default='')

    def __str__(self):
        return "%s %s %s %s %s" % (self.priority, self.table, self.ipv, self.chain, self.rule_value)


class Ouser(models.Model):
    name = models.CharField(max_length=256, default='')
    ip = models.CharField(max_length=256, default='')

    def __str__(self):
        return "%s %s" % (self.name, self.ip)


class OnlineUser(models.Model):
    login = models.CharField(max_length=256, default='')
    r_ip = models.CharField(max_length=256, default='')
    v_ip = models.CharField(max_length=256, default='')
    online_since = models.CharField(max_length=256, default='')

    def __str__(self):
        return "%s %s %s %s" % (self.login, self.r_ip, self.v_ip, self.online_since)


class ContactList(ListView):
    paginate_by = 10
    model = Ouser
