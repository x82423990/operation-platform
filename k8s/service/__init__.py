from django.views.generic import TemplateView, View, ListView

from kubernetes import client, config
from django.http import JsonResponse
from kubernetes.client.rest import ApiException
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator


class SvcManagement(View):
    @method_decorator(login_required)
    def get(self, request, types):
        if types == "getsvclist":
            page = int(request.GET.get('page'))
            limit = int(request.GET.get('limit'))
            config.load_kube_config()
            v1 = client.CoreV1Api()
            dp_list = []
            res = dict()
            count = 0
            tmp = v1.list_service_for_all_namespaces().items
            try:
                for i in tmp:
                    ret = dict()
                    ret['name'] = i.metadata.name
                    ret['selector'] = str(i.spec.selector)
                    ret['cluster_ip'] = i.spec.cluster_ip
                    ret['group'] = i.metadata.namespace
                    dp_list.append(ret)
                    count += 1
                res['count'] = count
                res["code"] = 0
                start_page = page * limit - limit
                end_page = page * limit
                res['data'] = dp_list[start_page: end_page]
            except Exception as e:
                print(e)
            return JsonResponse(res, safe=False)

    @method_decorator(login_required)
    def post(self, request, types):
        if types == 'del':
            ret = {'status': 0}
            ns = request.POST.get('group')
            svc_name = request.POST.get('name')
            print(svc_name, ns)
            try:
                config.load_kube_config()
                api_instance = client.CoreV1Api()
                body = client.V1DeleteOptions()
                api_instance.delete_namespaced_service(name=svc_name, namespace=ns, body=body)
            except ApiException as e:
                tmp = eval(str(e.body))
                ret['status'] = tmp.get('code')
                ret['msg'] = tmp.get('message')
            return JsonResponse(ret, safe=True)
        if types == 'add':
            ret = dict()
            ret["status"] = 0
            ns = request.POST.get('ns')
            labels = request.POST.get('selector')
            if request.POST.get('name'):
                name = request.POST.get('name')
            else:
                name = labels
            ports = int(request.POST.get('port'))
            target = int(request.POST.get('target'))
            try:
                config.load_kube_config()
                api_instance = client.CoreV1Api()
                service = client.V1Service()
                service.api_version = "v1"
                service.kind = "Service"
                service.metadata = client.V1ObjectMeta(name=name)
                spec = client.V1ServiceSpec()
                spec.selector = {"app": labels}
                spec.ports = [client.V1ServicePort(protocol="TCP", port=ports, target_port=target)]
                service.spec = spec
                api_instance.create_namespaced_service(namespace=ns, body=service)
                ret['msg'] = "服务创建成功"

            except ApiException as e:
                tmp = eval(str(e.body))
                ret['status'] = tmp.get('code')
                ret['msg'] = tmp.get('message')
            return JsonResponse(ret, safe=True)
