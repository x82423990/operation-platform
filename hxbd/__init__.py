from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required, login_required


def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    print(username, password)
    ret = dict()
    if user is not None:
        login(request, user)
        session_key = request.session.session_key
        print("sessionid.是:", session_key)
        ret["code"] = 0
        ret["msg"] = "success"
        ret['data'] = {"sessionid": session_key}
    else:
        ret["code"] = 1
        ret["msg"] = "用户名或者密码错误！"
        ret['data'] = "None"
    return JsonResponse(ret)


# @method_decorator(login_required)
@login_required
def test(request):
    ret = dict()
    ret["code"] = 0
    ret["msg"] = "test successfully"
    session_key = request.session.session_key
    ret["sessionkey"] = session_key
    return JsonResponse(ret)


@login_required
def user_logout(request):
    logout(request)
    return JsonResponse({"code": 0, "msg": "success"})