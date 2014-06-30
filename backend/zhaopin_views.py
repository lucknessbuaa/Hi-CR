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
from base.loggers import LOGGING


from base.models import City,Region,University
from base.utils import fieldAttrs,with_valid_form,RET_CODES
from backend.models import Zhaopin,TYPE_IN_JOB_CHOICES,EDUCATION_CHOICES
from backend import models

class ZhaopinForm(forms.ModelForm):
    
    pk = forms.IntegerField(required=False,
            widget=forms.HiddenInput(attrs=us.extend({},fieldAttrs)))

    name = forms.CharField(label=u'职位名称', 
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
                'parsley-required':'',
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
                'rows': '4',
           })))
    condition = forms.CharField(label=u'优先条件', required=False,
            widget=forms.Textarea(attrs=us.extend({}, fieldAttrs,{
                'rows': '4',
           })))
    class Meta:
        model = Zhaopin

class ZhaopinTable(tables.Table):
    ops = tables.columns.TemplateColumn(verbose_name=" 编辑",template_name='zhaopin_ops.html', orderable=False)

    class Meta:
        model = Zhaopin
        empty_text = u'no pages'
        orderable=False
        exclude=('id','pk','workdesc','jobdesc','condition')
        attrs = {
            'class': 'table table-bordered table-striped'
        }

@require_GET
@login_required
def pages(request):
    zhaopin = Zhaopin.objects.all()
    if 'q' in request.GET and request.GET['q'] <> "":
        message = request.GET['q']
        zhaopin = zhaopin.filter(Q(type__contains=message)|\
        Q(workdesc__contains=message)|\
        Q(jobdesc__contains=message))
    elif 'q' in request.GET and request.GET['q'] == "":
        return HttpResponseRedirect(request.path)
    table = ZhaopinTable(zhaopin)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    form = ZhaopinForm()
    return render(request, "zhaopin.html", {'table': table, 'form': form})
@require_POST
@login_required(login_url="/login.json")
@json
def add_page(request):
    def _add_page(form):
        zhaopin = form.save(commit=False)
        zhaopin.save()
        return {'ret_code': RET_CODES["ok"]}
    return with_valid_form(ZhaopinForm(request.POST), _add_page)


@require_POST
@login_required(login_url="/login.json")
@json
def edit_page(request, id):
    page = Zhaopin.objects.get(pk=id)
    form = ZhaopinForm(request.POST, instance=page)

    def _edit_page(form):
        form.save()
        return {'ret_code': RET_CODES["ok"]}

    return with_valid_form(form, _edit_page)


@require_POST
@login_required(login_url="/login.json")
@json
def delete_page(request):
    Zhaopin.objects.filter(pk=request.POST["id"]).delete()
    return {'ret_code': RET_CODES['ok']}
