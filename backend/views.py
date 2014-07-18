from django.shortcuts import render
from models import Jobs
from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ajax_add(request):
    response = HttpResponse()
    response['Content-Type']="text/javascript"
    if request.method == 'POST':
        job_id = request.POST.get('job_id',None)
        ret='haha'
        logger.debug(job_id)
        name_recommend = request.POST.get("name_recommend")
        mail_recommend = request.POST.get("mail_recommend")
        name = request.POST.get("name")
        school = request.POST.get("school")
        specialty = request.POST.get("specialty")
        tel = request.POST.get("tel")
        reason = request.POST.get("reason")
        date = request.POST.get("date")    
        logger.debug('receive success!')      
    ret+="send success!"
    response.write(ret)
    return response  
