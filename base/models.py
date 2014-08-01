# coding: utf-8
from django.db import models


class Region(models.Model):
    name = models.CharField(verbose_name=u'name', max_length=80, unique=True)

    def __unicode__(self):
        return self.name


class City(models.Model):
    region = models.ForeignKey(Region)
    name = models.CharField(verbose_name=u'name', max_length=80, unique=True)

    def __unicode__(self):
        return self.name


class University(models.Model):
    city = models.ForeignKey(City)
    name = models.CharField(verbose_name=u'name', max_length=100, unique=True)

    def __unicode__(self):
        return self.name
