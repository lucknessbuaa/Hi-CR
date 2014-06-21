from django.db import models

# Create your models here.
class Xuanjiang(models.Model):
    city = models.CharField(verbose_name=u'city', max_length=80)
    university = models.CharField(verbose_name=u'univercity', max_length=100)
    date = models.DateField()
    place = models.CharField(verbose_name=u'place',max_length=100)
    capacity = models.IntegerField() 
    speaker = models.CharField(verbose_name=u'speaker',max_length=100)
    wtdate = models.DateField()

class Zhaopin(models.Model):
    type = models.CharField(verbose_name=u'Type',max_length=50)
    place = models.CharField(verbose_name=u'Place',max_length=50)
    education = models.CharField(verbose_name=u'Education',max_length=50)
    number = models.IntegerField(verbose_name=u'The Number Of People')
    workdesc = models.CharField(verbose_name=u'Description',max_length=200,null=True,blank=True)
    jobdesc = models.CharField(verbose_name=u'Description',max_length=200,null=True,blank=True)
