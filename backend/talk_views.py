# coding: utf-8
import logging
from datetime import datetime

from underscore import _ as us
from django.db.models import Q
from django import forms
from django.core.cache import get_cache
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.conf import settings 
from django.utils.safestring import mark_safe
import django_tables2 as tables
from django_tables2 import RequestConfig
from django_render_json import json
from django.http import HttpResponseRedirect

from base.utils import fieldAttrs, with_valid_form, RET_CODES
from backend.models import Talk
from backend import models
from base.models import City, University

@require_GET
@login_required
def talk(request):
    talk = Talk.objects.all()
    if 'q' in request.GET and request.GET['q'] <> "":
        talk = talk.filter(Q(speaker__contains=request.GET['q'])|\
	Q(university__name__contains=request.GET['q'])|\
	Q(university__city_id__name__contains=request.GET['q'])|\
	Q(place__contains=request.GET['q']))
    elif 'q' in request.GET and request.GET['q'] == "":
        return HttpResponseRedirect(request.path)
    table = TalkTable(talk)
    form = TalkForm()
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "talk.html", {
        "table": table,
        "form": form
    })


class TalkTable(tables.Table):
    city = tables.columns.Column(verbose_name='城市', empty_values=(), orderable=False, accessor='university.city')
    university = tables.columns.Column(verbose_name='大学', empty_values=(), orderable=False)
    date = tables.columns.DateTimeColumn(verbose_name='宣讲会日期', empty_values=(), orderable=False, format='Y-m-d H:i')
    place = tables.columns.Column(verbose_name='地点', empty_values=(), orderable=False)
    capacity = tables.columns.Column(verbose_name='座位数', empty_values=(), orderable=False)
    speaker = tables.columns.Column(verbose_name='主讲人', empty_values=(), orderable=False)
    wtdate = tables.columns.DateTimeColumn(verbose_name='笔试时间', empty_values=(), orderable=False, format='Y-m-d H:i')
    ops = tables.columns.TemplateColumn(verbose_name='编辑', template_name='talk_ops.html', orderable=False)

    class Meta:
        model = Talk
        empty_text = u'no talk message'
        fields = ( "city", "university", "date", "place", "capacity", "speaker", "wtdate", )
        attrs = {
            'class': 'table table-bordered table-striped'
        }


class TalkForm(forms.ModelForm):

    pk = forms.IntegerField(required=False,
        widget=forms.HiddenInput(attrs=us.extend({}, fieldAttrs)))

    city = forms.CharField(label=u'城市',
        widget=forms.HiddenInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        }))) 

    university = forms.CharField(label=u'大学',
        widget=forms.HiddenInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))

    date = forms.DateTimeField(label="宣讲会日期", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    place = forms.CharField(label=u"地点",
        widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))

    capacity = forms.IntegerField(label=u"座位数",
        widget=forms.NumberInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))
    speaker = forms.CharField(label=u"主讲人", required=False,
        widget=forms.TextInput(attrs=us.extend({}, fieldAttrs, {
            'parsley-required': '',
        })))

    wtdate = forms.DateTimeField(label=u"笔试时间", input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Talk

@require_POST
@json
def add_talk(request):

    def _add_talk(form):
        talk = form.save(commit=False)
        form.save()
        return {'ret_code': RET_CODES["ok"]}

    return with_valid_form(TalkForm(request.POST), _add_talk)

@require_POST
@json
def delete_talk(request):
    Talk.objects.filter(pk=request.POST["id"]).delete()
    return {'ret_code': RET_CODES['ok']}

@require_POST
@json
def requireUni(request):
    selectUni = University.objects.all()

    def mapUni(uni):
        return {
            'id': 'U' + str(uni.pk),
            'type': 'university',
            'name': uni.name,
            'city': uni.city_id,
            'text': uni.name
        }

    selectUni = map(mapUni, selectUni)
    return {
        'ret_code': RET_CODES['ok'],
        'selectUni': selectUni
    }

@require_POST
@json
def requireCity(request):
    selectCity = City.objects.all()

    def mapCity(city):
        return {
            'id': 'C' + str(city.pk),
            'type': 'city',
            'name': city.name,
            'text': city.name
        }

    selectCity = map(mapCity, selectCity)
    return {
        'ret_code': RET_CODES['ok'],
        'selectCity': selectCity
    }

@require_POST
@json
def edit_talk(request, id):
    talk = Talk.objects.get(pk=id)
    form = TalkForm(request.POST, instance=talk)

    def _edit_talk(form):
        form.save()
        return {'ret_code': RET_CODES["ok"]}

    return with_valid_form(form, _edit_talk)


