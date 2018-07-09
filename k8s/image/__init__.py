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
            res = dict()
            res["code"] = 0
            try:
                pj_id = request.GET.get('pid', None)
                a = repitl.get_image_name(project_id=pj_id)
                ret['data'] = a
                res['data'] = ret
            except Exception as e:
                res["code"] = 2
                res["msg"] = "error"

            return JsonResponse(res)

        if types == 'tags':
            ret = dict()
            res = dict()
            try:
                repo_name = request.GET.get('image')
                tags = repitl.get_tags(repo_name)
                res["code"] = 0
                ret["data"] = tags
                res['data'] = ret
            except Exception as e:
                res["code"] = 2
                res["msg"] = "error"
            return JsonResponse(res)

        if types == 'project':
            res =dict()
            res['code'] = 0
            res['data'] = repitl.get_project()
            return JsonResponse(res)

        else:
            return JsonResponse({"code": 404, "msg": "你访问的页面的不存在!"})
