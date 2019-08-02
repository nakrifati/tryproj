from django.db import models


class Subscribers1(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=128)




