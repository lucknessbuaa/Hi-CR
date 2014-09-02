import json
import logging
import uuid

from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


from ajax_upload.forms import UploadedFileForm

from pybcs.bcs import BCS
from pybcs.bucket import Bucket

logger = logging.getLogger(__name__)
bcs = BCS(settings.BCS_HOST, settings.BCS_AK, settings.BCS_SK)
bucket = Bucket(bcs, settings.BCS_BUCKET)

@csrf_exempt
@require_POST
def upload(request):
    form = UploadedFileForm(data=request.POST, files=request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest(json.dumps({'errors': form.errors}))

    uploaded_file = form.save()
    logger.debug(uploaded_file.file.path)
    obj_name = str(uuid.uuid4())
    item = bucket.object('/' + obj_name)
    result = item.post_file(uploaded_file.file.path.encode('utf-8'))
    logger.debug(result)

    if result['status'] != 200:
        return HttpResponse(status=500)

    return HttpResponse(json.dumps({
        'path': 'http://' + settings.BCS_HOST + '/' + settings.BCS_BUCKET + '/' + obj_name
    }))

