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
from backend.models import Recommends, Consumer, JobAttention, Jobs, Talk, TalkSeats
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


class ConsumerForm(forms.ModelForm):
    class Meta:
        fields = ('email', 'phone', 'name')
        model = Consumer


def log_result(fn):
    def wrapper(request, *args, **kwargs):
        result = fn(request, *args, **kwargs)
        logger.debug("result: " +  str(result))
        return result

    return wrapper


@require_POST
@csrf_exempt
@ensure_consumer
@json
@log_result
def grab_talk(request, consumer):
    CODE_NOT_ALLOWD = 7001
    CODE_NO_MORE_SEATS = 7002
    CODE_DATA_INVALID = 1001

    form = ConsumerForm(request.POST, instance=consumer)
    if not form.is_valid():
        logger.warn("form is invalid")
        logger.warn(form.errors)
        return {'ret_code': CODE_DATA_INVALID}

    consumer = form.save()

    talkId = int(request.POST.get('talk'))
    talk = Talk.objects.get(pk=talkId)
    if not talk.grabbing:
        return {'ret_code': CODE_NOT_ALLOWD}

    leftSeats = talk.leftSeats()
    logger.debug("talk " + str(talkId) + " left seats" + str(leftSeats))
    if leftSeats <= 0:
        return {'ret_code': CODE_NO_MORE_SEATS}

    TalkSeats(talk=talk, consumer=consumer).save()
    return {'ret_code': 0}


@require_POST
@csrf_exempt
@ensure_consumer
@json
def giveup_talk(request, consumer):
    talkId = int(request.POST.get('talk'))
    talk = Talk.objects.get(pk=talkId)
    TalkSeats.objects.filter(talk=talk, consumer=consumer).delete()
    return {'ret_code': 0}



@require_POST
@csrf_exempt
@ensure_consumer
@json
def attention(request, consumer):
    jobId = int(request.POST.get('job'))
    consumer.attention(jobId)
    return {'ret_code': 0}


@require_GET
@json
def attention_count(request):
    jobId = int(request.GET.get('job'))
    job = Jobs.objects.get(pk=jobId)
    male = JobAttention.objects.filter(job=job, consumer__gender=1).count();
    female = JobAttention.objects.filter(job=job, consumer__gender=2).count();
    return {
        'ret_code': 0,
        'female': female,
        'male': male
    }


@require_GET
def csv(request):
    pass
