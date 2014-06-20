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
