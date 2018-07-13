# from server.models import Node as server
from server.models import Node
from django.http import JsonResponse
from django.views.generic import View


class NodeOperating(View):
    def get(self, request, types):
        # 添加node
        if types == "list":
            ret = dict()
            # already_exists = []
            # for i in server.objects.all():
            #     already_exists.append(i.name)
            ret['code'] = 0
            ret['data'] = 0
            return JsonResponse(ret)

        if types == "add":
            # node = request.GET.get('node', None)
            #
            # already_exists = []
            # for i in server.objects.all():
            #     already_exists.append(i.name)
            #     # print(already_exists, type(already_exists))
            # if node in already_exists:
            #     return JsonResponse({"code": 0, "msg": "node is already exists"})
            # # 初始化数据库
            # data = server(name=node)
            # data.save()
            return JsonResponse({"code": 0, "msg": "%s is add success" % node})
