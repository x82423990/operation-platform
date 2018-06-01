from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.sessions.models import Session



def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    print(username, password)
    ret = dict()
    if user is not None:
        login(request, user)
        ret["code"] = 0
        ret["msg"] = "success"
        # ret["session"] = request.SESSION_KEY
        # s = Session.objects.all()
        # ret["data"] = s

        # res = redirect("/")
        # res.set_cookie("username", username)
        # res.status_code = 200
        # return res


    else:
        ret["code"] = 1
        ret["msg"] = "forbbden"
    return JsonResponse(ret)


