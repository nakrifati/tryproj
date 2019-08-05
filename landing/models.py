from django.db import models


class Subscriber(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=128)

    def __str__(self):
        return "%s %s %s" % (self.name, self.email, self.id)


class Rule(models.Model):
    priority = models.CharField(max_length=256, default='')
    table = models.CharField(max_length=256, default='')
    ipv = models.CharField(max_length=64, default='')
    chain = models.CharField(max_length=256, default='')
    rule_value = models.CharField(max_length=256, default='')

    def __str__(self):
        return "%s %s %s %s %s" % (self.priority, self.table, self.ipv, self.chain, self.rule_value)
