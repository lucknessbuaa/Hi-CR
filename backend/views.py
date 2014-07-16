from django.shortcuts import render
from models import Jobs
from django.http import HttpResponse

def ajax_add(request):
    response = HttpResponse()
    response['Content-Type']="text/javascript"
    if request.is_ajax() and request.method == 'POST':
        title = request.POST.get("title") 
    ret="0"
    response.write(ret)
    return response  
