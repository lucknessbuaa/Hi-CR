import json
import logging

from django.http import HttpResponse
from django.db import models
from django.contrib.contenttypes.models import ContentType


logger = logging.getLogger(__name__)

fieldAttrs = {
    'class': 'form-control'
}

RET_CODES = {
    "ok": 0,
    "error": 1000,
    "auth-failure": 1001,
    "form-invalid": 1002
}


def with_valid_form(form, fn):
    if not form.is_valid():
        logger.warn("invalid form")
        logger.warn(form.errors);
        return {
            'ret_code': RET_CODES["form-invalid"],
            'form_errors': form.errors
        }   

    return fn(form)
