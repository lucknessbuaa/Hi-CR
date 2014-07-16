# coding: utf-8
from django.db import models
from base.models import City
class Talk(models.Model):
    city = models.CharField(verbose_name=u'city', max_length=80)
    university = models.CharField(verbose_name=u'univercity', max_length=100)
    date = models.DateField()
    place = models.CharField(verbose_name=u'place', max_length=100)
    capacity = models.IntegerField() 
    speaker = models.CharField(verbose_name=u'speaker', max_length=100)
    wtdate = models.DateField()

PRODUCT = 'PR'
TECNOLO = 'TE'
EXPRIEN = 'EX'
SUPPORT = 'SU'
TYPE_IN_JOB_CHOICES = ( 
    (TECNOLO,'技术'),
    (PRODUCT,'产品'),
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

class Jobs(models.Model):
    name = models.CharField(verbose_name=u'职位名称', max_length=50)
    judge = models.BooleanField(verbose_name=u'是否是实习')
    place = models.ForeignKey(City,related_name="工作地点", verbose_name=u'工作地点')
    type = models.CharField(verbose_name=u'工作类型', choices=TYPE_IN_JOB_CHOICES, max_length=5)
    education = models.CharField(verbose_name=u'学历要求', choices=EDUCATION_CHOICES,max_length=5)
    number = models.IntegerField(verbose_name=u'招聘人数',max_length=100, null=True , blank=True)
    examplace = models.ForeignKey(City,related_name="笔面试地点", verbose_name=u'笔面试地点')
    workdesc = models.TextField(verbose_name=u'工作职责', max_length=500, null=True, blank=True)
    jobdesc = models.TextField(verbose_name=u'职位要求', max_length=500, null=True, blank=True)
    condition = models.TextField(verbose_name=u'优先条件', max_length=500, null=True, blank= True)
    
#class Commend(models.Model):
#    mail_a = models.CharField(verbose_name=u'推荐人邮箱',max_length=50)
#    mail_b = models.CharField(verbose_name=u'邮箱',max_length=50)
#    name = models.CharField(verbose_name=u'姓名',max_length=50)    
#    school = models.CharField(verbose_name=u'高校',max_length=50) 
