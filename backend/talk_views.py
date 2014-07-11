# coding: utf-8
import logging

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


from base.utils import fieldAttrs
from backend.models import Talk
from backend import models
from base.models import City

@require_GET
@login_required
def talk(request):
    talk = Talk.objects.all()
    if 'q' in request.GET and request.GET['q'] <> "":
        talk = Talk.filter(Q(name__contains=request.GET['q'])|\
	Q(text__contains=request.GET['q'])|\
	Q(response__contains=request.GET['q']))
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
    city = tables.columns.Column(verbose_name='City', empty_values=(), orderable=False)
    university = tables.columns.Column(verbose_name='University', empty_values=(), orderable=False)
    date = tables.columns.Column(verbose_name='Date', empty_values=(), orderable=False)
    place = tables.columns.Column(verbose_name='Place', empty_values=(), orderable=False)
    capacity = tables.columns.Column(verbose_name='Capacity', empty_values=(), orderable=False)
    speaker = tables.columns.Column(verbose_name='主讲人', empty_values=(), orderable=False)
    wtdate = tables.columns.Column(verbose_name='笔试时间', empty_values=(), orderable=False)


    def render_inputType(self, **kwargs):
        record = kwargs["record"]
        logger.debug(record)
        return 'EVENT' if record.getInputType() == Dialog.INPUT_EVENT else 'TEXT' 

    def render_outputType(self, **kwargs):
        record = kwargs["record"]
        return 'PAGE' if record.getOutputType() == Dialog.OUTPUT_PAGE else 'TEXT'

    def render_inputMsg(self, **kwargs):
        record = kwargs["record"]
        return record.getInput()

    class Meta:
        model = Talk
        empty_text = u'no talk message'
        fields = ( "city", "university", "date", "place", "capacity", "speaker", "wtdate", )
        attrs = {
            'class': 'table table-bordered table-striped'
        }


class TalkForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all())

    university = forms.ModelChoiceField(queryset=City.objects.all())

    date = forms.DateField()

    def clean(self):
        cleaned_data = self.cleaned_data = super(TalkForm, self).clean()
        logger.debug(cleaned_data)

        return cleaned_data


def add_dialog(request):

    def _add_dialog(form):
        try:
            models.add_dialog(form)
            return {'ret_code': CODE_OK}
        except EventKeyDuplicatedError:
            return {'ret_code': CODE_EVENTKEY_DUPLICATED}
        except SubscribeDuplicatedError:
            return {'ret_code': CODE_SUBSCRIBE_DUPLICATED}

    return with_valid_form(TalkForm(request.POST), _add_dialog)
