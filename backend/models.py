# coding: utf-8
import logging
from django.db import models
from datetime import datetime

from base.models import City, University


logger = logging.getLogger(__name__)


class Talk(models.Model):
    university = models.ForeignKey(University,verbose_name=u'university',max_length=100)
    date = models.DateTimeField()
    place = models.CharField(verbose_name=u'place',max_length=100)
    cover = models.CharField(verbose_name=u'地点图片',max_length=1024)
    capacity = models.IntegerField(null=True,blank=True) 
    speaker = models.CharField(verbose_name=u'speaker',max_length=100,null=True,blank=True)
    wtdate = models.DateTimeField()

    grabbing = models.BooleanField(verbose_name=u'开放抢座', default=False)
    seats = models.IntegerField(verbose_name=u'抢座数量', default=0)

    def grabbedSeats(self):
        return TalkSeats.objects.filter(talk=self).count()

    def leftSeats(self):
        return self.seats - self.grabbedSeats()


class ConsumerManager(models.Manager):

    def ensureConsumer(self, token):
        try:
            return self.get(token=token)
        except:
            consumer = Consumer(token=token)
            consumer.save()
            return consumer


class Consumer(models.Model):
    token = models.CharField(unique=True, max_length=255)
    gender = models.IntegerField(verbose_name=u'性别', default=1, 
                                  choices=((1, u'男'), (2, u'女')))
    email = models.EmailField(verbose_name=u'邮箱')
    name = models.CharField(verbose_name=u'姓名', max_length=50)
    phone = models.CharField(verbose_name=u'电话号码', max_length=50)

    objects = ConsumerManager()

    def attention(self, jobId):
        job = Jobs.objects.get(pk=jobId)
        JobAttention(job=job, consumer=self).save()


class TalkSeats(models.Model):
    talk = models.ForeignKey(Talk)
    consumer = models.ForeignKey(Consumer)

    class Meta:
        unique_together = ('talk', 'consumer')


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

    def __unicode__(self):
        return self.name


class JobAttention(models.Model):
    job = models.ForeignKey(Jobs)
    consumer = models.ForeignKey(Consumer)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'consumer')

    
#class Commend(models.Model):
#    mail_a = models.CharField(verbose_name=u'推荐人邮箱',max_length=50)
#    mail_b = models.CharField(verbose_name=u'邮箱',max_length=50)
#    name = models.CharField(verbose_name=u'姓名',max_length=50)    
#    school = models.CharField(verbose_name=u'高校',max_length=50)

    
class Recommends(models.Model):
    jobId = models.IntegerField(verbose_name=u'职位ID')
    jobName = models.CharField(verbose_name=u'职位名称', max_length=50,null=True, blank=True)
    jobPlace = models.CharField(verbose_name=u'工作地点', max_length=50,null=True, blank=True)
    jobType = models.CharField(verbose_name=u'工作类型', max_length=10,null=True, blank=True)
    jobDesc = models.TextField(verbose_name=u'职位要求', max_length=500, null=True, blank=True)
    workDesc = models.TextField(verbose_name=u'工作职责', max_length=500, null=True, blank=True)
    condition = models.TextField(verbose_name=u'优先条件', max_length=500, null=True, blank= True)
    nameA = models.CharField(verbose_name=u'推荐人姓名', max_length=50)
    mailA = models.EmailField(verbose_name=u'推荐人邮箱', max_length=75)
    name = models.CharField(verbose_name=u'被推荐人姓名', max_length=50)
    mail = models.EmailField(verbose_name=u'被推荐人邮箱', max_length=75)
    tel = models.CharField(verbose_name=u'被推荐人电话', max_length=20)
    school = models.TextField(verbose_name=u'被推荐人大学', max_length=100)
    specialty = models.TextField(verbose_name=u'被推荐人专业', max_length=100)
    reason = models.TextField(verbose_name=u'推荐理由', max_length=500)
    date = models.DateField(verbose_name=u'推荐日期')
     
