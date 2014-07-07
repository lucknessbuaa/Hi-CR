# coding: utf-8
from django.db import models
from datetime import datetime
#from base.loggers import 
from base.models import City, University

class Talk(models.Model):
    university = models.ForeignKey(University,verbose_name=u'university',max_length=100)
    date = models.DateTimeField()
    place = models.CharField(verbose_name=u'place',max_length=100)
    capacity = models.IntegerField(null=True,blank=True) 
    speaker = models.CharField(verbose_name=u'speaker',max_length=100,null=True,blank=True)
    wtdate = models.DateTimeField()

PRODUCT = 'PR'
TECNOLO = 'TE'
EXPRIEN = 'EX'
SUPPORT = 'SU'
TYPE_IN_JOB_CHOICES = ( 
    (PRODUCT,'产品'),
    (TECNOLO,'技术'),
    (EXPRIEN,'用户体验'),
    (SUPPORT,'管理支持')
) 

EDUCATION_CHOICES = (
    ('QT','无学历要求'),
    ('DZ','大专'),
    ('BK','本科'),
    ('SS','硕士'),
    ('BS','博士')
)

class Zhaopin(models.Model):
    name = models.CharField(verbose_name=u'职位名称',max_length=50)
    judge = models.BooleanField(verbose_name=u'是否是实习')
 
    place = models.ForeignKey(City,related_name="工作地点",verbose_name=u'工作地点')
    type = models.CharField(verbose_name=u'工作类型',choices=TYPE_IN_JOB_CHOICES,default = 0, max_length=5)
    education = models.CharField(verbose_name=u'学历要求',choices=EDUCATION_CHOICES,max_length=5)
    number = models.IntegerField(verbose_name=u'招聘人数')
    examplace = models.ForeignKey(City,related_name="笔面试地点",verbose_name=u'笔面试地点')
    workdesc = models.TextField(verbose_name=u'工作职责',max_length=500,null=True,blank=True)
    jobdesc = models.TextField(verbose_name=u'职位要求',max_length=500,null=True,blank=True)
    condition = models.TextField(verbose_name=u'优先条件',max_length=500,null=True,blank= True) 
