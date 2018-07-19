# from server.models import Node as server
from server.models import Node as server
from server.models import NodeInfo, MonitorInfo
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.generic import View
from nodeApi import Node
from django.core import serializers


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
                # 保存服务器到数据库
                data = server(name=node)
                data.save()
                # 获取硬件信息到nodeinfo 里面
                # ser = NodeInfo.objects.get(server_name=data)
                info = Node().list(node)[0]
                print(info)
                obj = NodeInfo(server_name=data, env=info.get('env'), IP=info.get('ip'), job=info.get('job'),
                               position=info.get('position'))
                obj.save()
            except (TypeError, IntegrityError):
                return JsonResponse({"code": 3, "msg": "params err"})

            return JsonResponse({"code": 0, "msg": "%s is add success" % node})
        if types == "flush":
            n = Node()
            already_exists = self.__getall()
            for i in already_exists:
                ser = server.objects.get(name="master")
                info = n.list(i)[0]
                try:
                    obj = NodeInfo.objects.get(server_name=ser)
                    print(obj is None)
                except server.DoesNotExist:
                    return JsonResponse({"code": 404})
                if info:
                    try:
                        print(obj.env)
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
        if types == "list_online":
            node_all = Node().list()
            node_list = []
            for n in node_all:
                node = n.get("instance")
                print(node)
                node_list.append(node)
            return JsonResponse({"code": 0, "data": node_list})
        # 没有匹配到则返回404
        return JsonResponse({"code": 404, "msg": 'page not found'})

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


class Monitor(View):
    def __getall(self):
        already_exists = []
        for i in server.objects.all():
            already_exists.append(i.name)
        return already_exists

    def get(self, request, types):

        if types == "flush":
            n = Node()
            server_list = self.__getall()
            for j in server_list:
                ser = server.objects.get(name=j)
                i = n.monitor(j)
                monitor_info = MonitorInfo(count_cpu=i.get("count_cpu"), load=i.get("load5"),
                                           total_mem=i.get("total_mem"), available_mem=i.get("available_mem"),
                                           get_time=i.get("current_time"), server_name=ser,
                                           available_disk=i.get("available_disk"), total_disk=i.get("total_disk"))
                monitor_info.save()
            return JsonResponse({"code": 0, "msg": "flush success!"})

        if types == "list":
            node = request.GET.get('name', None)
            last = request.GET.get('name')
            start = request.GET.get('start')
            end = request.GET.get('end')
            try:
                ser = server.objects.get(name=node)
            except (IntegrityError, server.models.DoesNotExis, AttributeError):
                return JsonResponse("err")
            ret = MonitorInfo.objects.filter(server_name=ser).order_by("get_time")
            ret2 = MonitorInfo.objects.filter(server_name=ser).values().order_by("get_time")
            print(ret2)
            # print(ret.objects.get(all()))
            # 转换成UTC， 强制
            # print(ret.get_time.replace(tzinfo=timezone.utc))
            # UTC强制转换utc-8
            # print(ret.get_time.astimezone(timezone(timedelta(hours=8))))
            tmp = eval(serializers.serialize("json", ret))
            data = dict()
            data["code"] = 0
            data["data"] = tmp
            return JsonResponse(data)
        return JsonResponse({"code": 404, "msg": "objects not found."})
