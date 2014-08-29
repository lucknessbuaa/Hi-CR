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
from backend.models import Recommends, Consumer
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
        return redirect("/backend/reports")

    stop = form.cleaned_data["stop"]
    
    start = form.cleaned_data["start"]
    recommend = Recommends.objects.filter(date__gte=start, date__lte=stop).order_by('-pk')
    table = RecommendTable(recommend)
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    form = FilterForm({
        'start': datetime.strftime(start, "%Y-%m-%d"),
        'stop': datetime.strftime(stop, "%Y-%m-%d"),
    })
    return render(request, "recommend.html", {
        "table": table,
        "form": form,
    })


class AttentionTable(tables.Table):
    class Meta:
        model = Recommends
        empty_text = u'没有关注记录'
        orderable = False
        fields = ('id','jobName','jobPlace','jobType','mailA','name','mail','date')
        exclude=('pk','jobId','jobDesc','workDesc','condition','nameA')
        attrs = {
            'class': 'table table-bordered table-striped'
        }


def ensure_consumer(fn):
    def wrapper(request, *args, **kwargs):
        token = request.POST.get('token', None)
        if not token:
            return render_json({'ret_code': 3001})

        consumer = Consumer.objects.ensureConsumer(token)
        return fn(request, consumer, *args, **kwargs)

    return wrapper


@require_GET
@json
def total(request):
    return {'ret_code': 0, 'total': Consumer.objects.all().count()}


@require_POST
@csrf_exempt
@ensure_consumer
@json
def gender(request, consumer):
    gender = int(request.POST.get('gender', '0'))
    if gender != 1 and gender != 2:
        return {'ret_code': 1001}

    consumer.gender=gender
    consumer.save()
    return {'ret_code': 0}



@require_POST
@csrf_exempt
@ensure_consumer
@json
def gender(request, consumer):
    gender = int(request.POST.get('gender', '0'))
    if gender != 1 and gender != 2:
        return {'ret_code': 1001}

    consumer.gender=gender
    consumer.save()
    return {'ret_code': 0}


@require_GET
def csv(request):
    pass
