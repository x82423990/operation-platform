from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect


def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    ret = dict()
    if user is not None:
        login(request, user)
        ret["code"] = 0
        ret["msg"] = "success"
        res = redirect("/static/index.html")
        res.set_cookie("username", username)
        res.status_code = 200
        return res
    else:
        ret["code"] = 1
        ret["msg"] = "forbbden"
        return JsonResponse(ret)
