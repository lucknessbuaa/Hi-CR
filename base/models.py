# coding: utf-8
from django.db import models

# Create your models here.

class Region(models.Model):
    name = models.CharField(verbose_name=u'name', max_length=80, unique=True)


class City(models.Model):
    region = models.ForeignKey(Region)
    name = models.CharField(verbose_name=u'name', max_length=80, unique=True)


class University(models.Model):
    city = models.ForeignKey(City)
    name = models.CharField(verbose_name=u'name', max_length=100, unique=True)
