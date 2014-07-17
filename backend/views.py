from django.shortcuts import render
from models import Jobs
from django.http import HttpResponse

def ajax_add(request):
    response = HttpResponse()
    response['Content-Type']="text/javascript"
    if request.is_ajax() and request.method == 'POST':
        job_id = request.POST.get("job_id")
        name_recommend = request.POST.get("name_recommend")
        mail_recommend = request.POST.get("mail_recommend")
        name = request.POST.get("name")
        school = request.POST.get("school")
        specialty = request.POST.get("specialty")
        tel = request.POST.get("tel")
        reason = request.POST.get("reason")
        date = request.POST.get("date")    
       
    ret="0"
    response.write(ret)
    return response  
