# encoding: utf-8
import time
import logging

from django.db.models import Q
from django import forms
from django.core.cache import get_cache
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.conf import settings
from django.utils.safestring import mark_safe
import django_tables2 as tables
from django_tables2 import RequestConfig
from underscore import _ as us
from django_render_json import json
from django.http import HttpResponseRedirect
from baidu.loggers import LOGGING

from base.decorators import active_tab
from base.models import City,Region,University
from base.utils import fieldAttrs,with_valid_form,RET_CODES
from backend.models import Jobs,TYPE_IN_JOB_CHOICES,EDUCATION_CHOICES
from backend import models

class JobsForm(forms.ModelForm):
    
    pk = forms.IntegerField(required=False,
            widget=forms.HiddenInput(attrs=us.extend({},fieldAttrs)))

    name = forms.CharField(label=u'职位名称',max_length=20, 
            widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
                'parsley-required':'',
            })))

    judge = forms.BooleanField(label=u'是否实习',required=False)
    
    place = forms.ModelChoiceField(queryset=City.objects.all(),label=u'工作地点',
            widget=forms.Select(attrs=us.extend({},fieldAttrs,{
                'parsley-required':'',
            })))
    type = forms.ChoiceField(choices=TYPE_IN_JOB_CHOICES,label=u'工作类型',
            widget=forms.Select(attrs=us.extend({},fieldAttrs,{
                'parsley-required':'',
            })))

    education = forms.ChoiceField(choices=EDUCATION_CHOICES,label=u'学历要求',
            widget=forms.Select(attrs=us.extend({},fieldAttrs,{
                'parsley-required':'',
            }))) 
   
    number = forms.IntegerField(label=u'招聘人数',required=False,
            widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
            })))
    examplace = forms.ModelChoiceField(queryset=City.objects.all(),label=u'笔面试地点',
            widget=forms.Select(attrs=us.extend({},fieldAttrs,{
                'parsley-required':'',
            })))

    workdesc = forms.CharField(label=u'工作职责', required=False,
            widget=forms.Textarea(attrs=us.extend({}, fieldAttrs,{
                'parsley-required': '', 
                'rows': '4',
                'style': 'resize:none'  
           })))
    jobdesc = forms.CharField(label=u'职位要求', required=False,
            widget=forms.Textarea(attrs=us.extend({}, fieldAttrs,{
                'parsley-required': '', 
                'rows': '4',
                'style': 'resize:none' 
           })))
    condition = forms.CharField(label=u'优先条件', required=False,
            widget=forms.Textarea(attrs=us.extend({}, fieldAttrs,{
                'parsley-required': '', 
                'rows': '4',
                'style': 'resize:none' 
           })))
    class Meta:
        model = Jobs

class JobsTable(tables.Table):
    number = tables.Column(empty_values=())
    ops = tables.columns.TemplateColumn(verbose_name=" 操作",template_name='jobs_ops.html', orderable=False) 
    def render_judge(self,value):
        pd=value
        return mark_safe('<span class="glyphicon glyphicon-%s"></span>'% ("ok" if value==True else "remove"))
    def render_number(self,value):
        return "若干" if value==0 else  value 
    def render_name(self,record):
        st = "%s" %record.name
        st += (u"（实习）"if record.judge ==True else "")
        return st
    class Meta:
        model = Jobs
        empty_text = u'没有招聘信息'
        orderable=False
        exclude=('judge','id','pk','workdesc','jobdesc','condition')
        attrs = {

            'class': 'table table-bordered table-striped'
        }

@require_GET
@login_required
@active_tab('jobs')
def jobs(request):
    jobs = Jobs.objects.all()
    if 'q' in request.GET and request.GET['q'] <> "":
        message = request.GET['q']
        jobs = jobs.filter(Q(type__contains=message)|\
                           Q(number__contains=message)|\
                           Q(education__contains=message)|\
                           Q(name__contains=message))   
    elif 'q' in request.GET and request.GET['q'] == "":
        return HttpResponseRedirect(request.path)
    table = JobsTable(jobs)
    if (jobs.count()==0 and request.GET['q'] <> "") :
        table.empty_text = u"没有搜索结果"
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    form = JobsForm()
    return render(request, "jobs.html", {'table': table, 'form': form})


@require_POST
@login_required(login_url="/login.json")
@json
def add_jobs(request):
    def _add_jobs(form):
        jobs = form.save(commit=False)
        jobs.save()
        return {'ret_code': RET_CODES["ok"]}
    return with_valid_form(JobsForm(request.POST), _add_jobs)


@require_POST
@login_required(login_url="/login.json")
@json
def edit_jobs(request, id):
    jobs = Jobs.objects.get(pk=id)
    form = JobsForm(request.POST, instance=jobs)

    def _edit_jobs(form):
        form.save()
        return {'ret_code': RET_CODES["ok"]}

    return with_valid_form(form, _edit_jobs)


@require_POST
@login_required(login_url="/login.json")
@json
def delete_jobs(request):
    Jobs.objects.filter(pk=request.POST["id"]).delete()
    return {'ret_code': RET_CODES['ok']}
