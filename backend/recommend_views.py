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
from django_render_csv import render_csv

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
    recommend = Recommends.objects.all()
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
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, "recommend.html", {
        "table": table,
    })


class RecommendTable(tables.Table):
    

    class Meta:
        model = Recommends
        empty_text = u'没有推荐信息'
        orderable=False
        exclude=('pk', 'id')
        attrs = {
            'class': 'table table-bordered table-striped'
        }


@require_GET
def csv(request):
    logs = Recommends.objects.all();
    
    logs = [['职位ID', '职位名称', '工作地点', '招聘人数', '工作类型', '职位要求','工作职责', '优先条件', '推荐人姓名', '推荐人邮箱', '被推荐人姓名', '被推荐人邮箱', '被推荐人大学', '被推荐人专业', '推荐理由', '推荐日期']] + map(lambda log: [
        log.jobId,
        log.jobName.encode('utf-8'),
        log.jobPlace.encode('utf-8'),
        log.jobNumber,
        log.jobType.encode('utf-8'),
        log.jobDesc.encode('utf-8'),
        log.workDesc.encode('utf-8'),
        log.condition.encode('utf-8'),
        log.nameA.encode('utf-8'),
        log.mailA.encode('utf-8'),
        log.name.encode('utf-8'),
        log.mail.encode('utf-8'),
        log.school.encode('utf-8'),
        log.specialty.encode('utf-8'),
        log.reason.encode('utf-8'),
        log.date,
    ], logs)

    filename = u"hello.csv"
    logger.debug("filename: " + filename)
    return render_csv(logs, filename=filename.encode('utf-8'))
