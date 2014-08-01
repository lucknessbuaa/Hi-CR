from django.shortcuts import render
from models import Jobs,Recommends
from base.models import City
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
        jobs = Jobs.objects.filter(id=job_id)
        jobs = jobs[0]
        job_name = jobs.name 
        place = City.objects.filter(id=jobs.place_id)
        job_place = place[0].name
        job_type = jobs.type
        job_jobdesc = jobs.jobdesc
        job_workdesc = jobs.workdesc
        job_condition = jobs.condition
        ret='congratulation.'
        logger.debug(jobs)
        name_recommend = request.POST.get("name_recommend")
        mail_recommend = request.POST.get("mail_recommend")
        name = request.POST.get("name")
        mail = request.POST.get("mail")
        school = request.POST.get("school")
        specialty = request.POST.get("specialty")
        tel = request.POST.get("tel")
        reason = request.POST.get("reason")
        date = request.POST.get("date")    
        logger.debug('receive success!')      
        Recommends(jobId=job_id,jobName=job_name,jobPlace=job_place,tel=tel,jobType=job_type,jobDesc=job_jobdesc,workDesc=job_workdesc,condition=job_condition,nameA=name_recommend,mailA=mail_recommend,name=name,mail=mail,school=school,specialty=specialty,reason=reason,date=date).save()
    ret+="send success!"
    response.write(ret)
    return response  
