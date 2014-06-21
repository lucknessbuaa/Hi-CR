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

from base.utils import fieldAttrs
from backend.models import Zhaopin
from backend import models

class ZhaopinForm(forms.ModelForm):
    
    type = forms.CharField(label=u'Type',
            widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
                'parsley-required': '',
            })))
    place = forms.CharField(label=u'Place', required=False,
            widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
                'parsley-required':'',
            })))
    education = forms.CharField(label=u'Education', required=False,
            widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
                'parsley-required':'',
            })))
    number = forms.IntegerField(label=u'Number',required=False,
            widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
                'parsley-required':'',
            })))
    workdesc = forms.CharField(label=u'Responsibility', required=False,
            widget=forms.TextInput(attrs=us.extend({}, fieldAttrs)))
    jobdesc = forms.CharField(label=u'Job', required=False,
            widget=forms.TextInput(attrs=us.extend({}, fieldAttrs)))
    class Meta:
        model = Zhaopin

class ZhaopinTable(tables.Table):
    ops = tables.columns.TemplateColumn(template_name='zhaopin_ops.html', orderable=False)

    class Meta:
        model = Zhaopin
        empty_text = u'no pages'
        orderable=False
        exclude=('id')
        attrs = {
            'class': 'table table-bordered table-striped'
        }

@require_GET
@login_required
def pages(request):
#    account = Account.objects.get(user__pk=request.user.pk)
#    pages = Page.objects.filter(account=account)
    zhaopin = Zhaopin.objects.all()
    if 'q' in request.GET and request.GET['q'] <> "":
        message = request.GET['q']
        zhaopin = Zhaopin.filter(Q(type__contains=message)|\
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
def add_page(request):
    #raise Exception()
    def _add_page(form):
        page = form.save(commit=False)
        page.account = Account.objects.get(user__pk=request.user.pk)
        page.save()
        return {'ret_code': RET_CODES["ok"]}
    return with_valid_form(PageForm(request.POST), _add_page)


@require_POST
@login_required(login_url="/login.json")
def edit_page(request, id):
    #raise Exception()
    #time.sleep(3)
    account = Account.objects.get(user__pk=request.user.pk)
    page = Page.objects.get(pk=id, account=account)
    form = PageForm(request.POST, instance=page)

    def _edit_page(form):
        form.save()
        if len(PageItem.objects.filter(page=page)) > 0:
            wps.emitChangeEvent(account)
        return {'ret_code': RET_CODES["ok"]}

    return with_valid_form(form, _edit_page)


@require_POST
@login_required(login_url="/login.json")
@json
def delete_page(request):
    #time.sleep(3)
    #raise Exception()
    account = Account.objects.get(user__pk=request.user.pk)
    Page.objects.filter(pk=request.POST["id"], account=account).delete()
    wps.emitChangeEvent(account)
    return {'ret_code': RET_CODES['ok']}
