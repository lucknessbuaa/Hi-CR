# coding: utf-8
import logging
from datetime import datetime
from datetime import date
from datetime import timedelta

from underscore import _ as us
from django.db.models import Q
from django import forms
from django.core.cache import get_cache
from django.core.urlresolvers import reverse
from django.db import InternalError
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.conf import settings 
from django.utils.safestring import mark_safe
import django_tables2 as tables
from django_tables2 import RequestConfig
from django_render_json import json, render_json
from django.http import HttpResponseRedirect
from django_render_csv import render_csv, as_csv

from base.decorators import active_tab
from base.utils import fieldAttrs, with_valid_form, RET_CODES
from backend.models import Recommends, Consumer, JobAttention, Jobs
from backend import models
from base.models import City, University

logger = logging.getLogger(__name__)


class FilterForm(forms.Form):
    start = forms.DateField(label="start", input_formats=["%Y-%m-%d"], 
        required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    stop = forms.DateField(label="stop", input_formats=["%Y-%m-%d"], 
        required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    
    def clean(self):
        data = super(FilterForm, self).clean()
        stop = data.get("stop", None)
        today = date.today()
        if stop is None:
            stop = today
        if stop > today:
            stop = today

        start = data.get("start", None)
        if start is None:
            start = stop - timedelta(days=7)

        if start > stop:
            start = stop

        return {
            "start": start,
            "stop": stop,
        }


@require_GET
@login_required
@active_tab('attention')
def attention(request):
    form = FilterForm(request.GET)
    if not form.is_valid():
        logger.warn("reports, form is invalid, " + str(form.errors))
        return redirect("/backend/attention")

    stop = form.cleaned_data["stop"]
    _stop = stop + timedelta(days=1)
    start = form.cleaned_data["start"]

    attentions = JobAttention.objects.filter(date__gte=start, date__lt=_stop).order_by('-pk')
    table = AttentionTable(attentions)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    form = FilterForm({
        'start': datetime.strftime(start, "%Y-%m-%d"),
        'stop': datetime.strftime(stop, "%Y-%m-%d"),
    })
    return render(request, "attention.html", {
        "table": table,
        "form": form,
    })


@require_GET
def csv(request):
    form = FilterForm(request.GET)
    if not form.is_valid():
        logger.warn("reports, form is invalid, " + str(form.errors))
        return redirect("/backend/reports")
    stop = form.cleaned_data["stop"]
    _stop = stop + timedelta(days=1)
    start = form.cleaned_data["start"]
    data = JobAttention.objects.filter(date__gte=start, date__lt=_stop).order_by('-pk')

    logs = [[u'职位ID', u'职位名称', u'用户', u'日期']] + map(lambda item: [
        item.job.pk,
        item.job.name,
        item.consumer.token,
        item.date.strftime('%Y-%m-%d %H:%M')
    ], data)

    filename = u"output.csv"
    logger.debug("filename: " + filename)
    return render_csv(logs, filename=filename.encode('utf-8'))


class AttentionTable(tables.Table):
    job = tables.Column(verbose_name = u'职位')
    consumer = tables.Column(verbose_name = u'用户')
    date = tables.Column(verbose_name=u'时间')

    def render_date(self, value):
        return value.strftime('%Y-%m-%d %H:%M') 

    class Meta:
        model = JobAttention
        empty_text = u'没有关注记录'
        fields = ('job', 'consumer', 'date')
        orderable = False
        attrs = {
            'class': 'table table-bordered table-striped'
        }

