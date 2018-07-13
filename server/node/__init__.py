# from server.models import Node as server
from server.models import Node as server
from server.models import NodeInfo
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.generic import View
from nodeApi import Node


class NodeOperating(View):

    def __getall(self):
        already_exists = []
        for i in server.objects.all():
            already_exists.append(i.name)
        return already_exists

    def get(self, request, types):
        # 添加node
        if types == "list":
            suc = dict()
            ret = dict()

            suc['code'] = 0
            ret['server'] = self.__getall()
            suc['data'] = ret
            return JsonResponse(suc)
        if types == "add":
            node = request.GET.get('name', None)

            already_exists = []
            for i in server.objects.all():
                already_exists.append(i.name)
                # print(already_exists, type(already_exists))
            if node in already_exists:
                return JsonResponse({"code": 2, "msg": "node is already exists"})
            # 初始化数据库
            try:
                data = server(name=node)
                data.save()
            except (TypeError, IntegrityError):
                return JsonResponse({"code": 3, "msg": "params err"})
            return JsonResponse({"code": 0, "msg": "%s is add success" % node})
        if types == "flush":
            n = Node()
            # obj = NodeInfo
            already_exists = self.__getall()
            print(already_exists)
            for i in already_exists:
                ser = server.objects.get(name=i)
                info = n.list(i)
                obj = NodeInfo.objects.get(server_name=ser)
                if info:
                    print(info)
                    try:
                        obj.env = info.get('env')
                        obj.IP = info.get('ip')
                        obj.job = info.get('job')
                        obj.position = info.get('position')
                        obj.save()
                    except IntegrityError:
                        return JsonResponse({"code": 4, "msg": "写入数据库错误!"})
                else:
                    return JsonResponse({"code": 4, "msg": "get server err!"})
            return JsonResponse({"code": 0, "msg": "flush success!"})

    def post(self, request, types):
        if types == "delete":
            node = request.POST.get('name', None)
            try:
                obj = server.objects.filter(name=node)
                obj.delete()
            except (TypeError, IntegrityError):
                return JsonResponse({"code": 3, "msg": "remove failed"})
            return JsonResponse({"code": 0, "msg": "success"})
        return JsonResponse({"code": 404, "msg": "objects not found."})
