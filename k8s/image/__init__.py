from django.views.generic import View
# from kubernetes import client, config
# import time
from django.http import JsonResponse
# from kubernetes.client.rest import ApiException
from k8s import hub as repitl

from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator


# from datetime import timedelta, timezone
# import json

class Image(View):
    @method_decorator(login_required)
    def get(self, request, types):
        if types == 'img':
            ret = dict()
            ret["code"] = 0
            try:
                pj_id = request.GET.get('pid', None)
                a = repitl.get_image_name(project_id=pj_id)
                print(a)
                ret['data'] = a
            except Exception as e:
                ret["code"] = 2
                ret["msg"] = "error"
            return JsonResponse(ret)

        if types == 'tags':
            ret = dict()
            try:
                repo_name = request.GET.get('image')
                tags = repitl.get_tags(repo_name)
                ret["code"] = 0
                ret["data"] = tags
            except Exception as e:
                ret["code"] = 2
                ret["msg"] = "error"
            print(ret)
            return JsonResponse(ret)

        if types == 'project':
            return JsonResponse(repitl.get_project())

        else:
            return JsonResponse({"code": 404, "msg": "你访问的页面的不存在!"})
