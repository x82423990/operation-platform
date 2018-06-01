from django.http import JsonResponse
from django.views.generic import View
import time
from datetime import timedelta, timezone
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator


class Nm_list(View):
    # @login_required()
    def get(self, request):
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        ret = dict()
        res = dict()
        nm_list = []
        counter = 0
        try:
            config.load_kube_config()
            v1 = client.CoreV1Api()
            # 好像米=前端模板不支持切面,这里把namespace 循环除来=加到nmlist里面
            for i in v1.list_namespace(watch=False).items:
                res = dict()
                res["namespace"] = i.metadata.name
                timeP = i.metadata.creation_timestamp.replace(tzinfo=timezone.utc).astimezone(
                    timezone(timedelta(hours=8)))
                times = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.mktime(timeP.timetuple())))
                res["time"] = times
                nm_list.append(res)
                counter += 1
            ret['code'] = 0
            ret['count'] = counter

        except ApiException as e:
            print(e)
            ret['code'] = 403
            ret['count'] = 0
            ret['data'] = e
        startPage = page * limit - limit
        endPage = startPage + limit
        ret['data'] = nm_list[startPage:endPage]
        return JsonResponse(ret, safe=True)

    def post(self, request, types):
        if types == "add":
            ret = {'status': 0}
            name = request.POST.get('ns', None)
            if name.isalpha():
                try:
                    # 实例化一个api配置
                    config.load_kube_config()
                    v1 = client.CoreV1Api()
                    # 实例化一个namespace对象
                    ns = client.V1Namespace()
                    ns.metadata = client.V1ObjectMeta(name=name)

                    # 生成namespace
                    v1.create_namespace(body=ns)
                    print(name)
                except ApiException as e:

                    tmp = eval(str(e.body))

                    ret['status'] = tmp.get('code')

                    ret['msg'] = tmp.get('message')
            else:
                ret['status'] = '8'
                ret['msg'] = "名称必须为纯字母"
            return JsonResponse(ret, safe=True)

        if types == "del":
            ret = {'code': 0}
            name = request.POST.get('ns', None)
            print(name)
            try:
                config.load_kube_config()
                v1 = client.CoreV1Api()
                ns = client.V1Namespace()
                v1.delete_namespace(body=ns, name=name)
                ret['msg'] = 'success'
            except ApiException as e:
                print(e)
                ret['code'] = 0
                ret['msg'] = 'error'
            return JsonResponse(ret, safe=True)
