import logging

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import django.contrib.auth as auth
from django_render_json import render_json


from base.utils import RET_CODES


logger = logging.getLogger(__name__)
def login(request):
    if request.method == 'GET':
        return render(request, "login.html")
    else:
        user = request.POST.get('user', None)
        password = request.POST.get('password', None)
        user = auth.authenticate(username=user, password=password)

        if not user:
            return render_json({'ret_code': RET_CODES["auth-failure"]})

        auth.login(request, user)
        return render_json({'ret_code': RET_CODES["ok"]})

def logout(request):
    auth.logout(request)
    return redirect('/welcome')

def welcome(request):
    if not request.user.is_authenticated():
        logger.warn("welcome: user is not authenticated")
        return redirect("/login")
    else:
        return render(request, "hello.html")

