# coding: utf-8
import logging
from datetime import datetime

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
from django_render_json import json
from django.http import HttpResponseRedirect
from django_render_csv import render_csv, as_csv

from base.decorators import active_tab
from base.utils import fieldAttrs, with_valid_form, RET_CODES
from backend.models import Recommends
from backend import models
from base.models import City, University

logger = logging.getLogger(__name__)

@require_GET
@login_required
@active_tab('recommend')
def recommend(request):
    recommend = Recommends.objects.all().order_by('-pk')
    search = False
    if 'q' in request.GET and request.GET['q'] <> "":
        logger.error(request.GET['q'])
        talk = talk.filter(Q(speaker__contains=request.GET['q'])|\
	Q(university__name__contains=request.GET['q'])|\
	Q(university__city_id__name__contains=request.GET['q'])|\
	Q(place__contains=request.GET['q']))
        if not talk.exists() :
            search = True
    elif 'q' in request.GET and request.GET['q'] == "":
        return HttpResponseRedirect(request.path)
    table = RecommendTable(recommend)
    if search :
        table = RecommendTable(recommend, empty_text='没有搜索结果')
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    return render(request, "recommend.html", {
        "table": table,
    })


class RecommendTable(tables.Table):
    

    class Meta:
        model = Recommends
        empty_text = u'没有推荐信息'
        orderable = False
        fields = ('id','jobName','jobPlace','jobType','mailA','name','mail','date')
        exclude=('pk','jobId','jobDesc','workDesc','condition','nameA')
        attrs = {
            'class': 'table table-bordered table-striped'
        }


@require_GET
def csv(request):
    logs = Recommends.objects.all();
    logs = [[u'职位ID', u'职位名称', u'工作地点', u'工作类型', u'职位要求',u'工作职责', u'优先条件', u'推荐人姓名', u'推荐人邮箱', u'被推荐人姓名', u'被推荐人邮箱', u'被推荐人电话',u'被推荐人大学', u'被推荐人专业', u'推荐理由', u'推荐日期']] + map(lambda log: [
        log.jobId,
        log.jobName,
        log.jobPlace,
        log.jobType,
        log.jobDesc,
        log.workDesc,
        log.condition,
        log.nameA,
        log.mailA,
        log.name,
        log.mail,
        log.tel,
        log.school,
        log.specialty,
        log.reason,
        log.date,
    ], logs)

    filename = u"output.csv"
    logger.debug("filename: " + filename)
    return render_csv(logs, filename=filename.encode('utf-8'))
