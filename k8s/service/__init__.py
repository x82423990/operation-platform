from django.views.generic import TemplateView, View, ListView

from kubernetes import client, config
from django.http import JsonResponse
from kubernetes.client.rest import ApiException
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator


class SvcManagement(View):
    @method_decorator(login_required)
    def get(self, request, types):
        if types == "list":
            page = request.GET.get('page')
            limit = request.GET.get('limit')
            keyword = request.GET.get('keyword')
            ns = request.GET.get('ns')
            config.load_kube_config()
            v1 = client.CoreV1Api()
            svc_list = []
            res = dict()
            sus = dict()
            count = 0
            if ns:
                tmp = v1.list_namespaced_service(namespace=ns).items
            else:
                tmp = v1.list_service_for_all_namespaces().items
            try:
                for i in tmp:
                    ret = dict()
                    ret['name'] = i.metadata.name
                    ret['selector'] = str(i.spec.selector)
                    ret['cluster_ip'] = i.spec.cluster_ip
                    ret['group'] = i.metadata.namespace
                    if keyword:
                        if keyword in ret.get('name'):
                            svc_list.append(ret)
                            count += 1
                    else:
                        svc_list.append(ret)
                        count += 1
                if count == 0:
                    return JsonResponse({"code": 404, "msg": " not found svc!"})
                res['count'] = count
                sus["code"] = 0
                page = int(page)
                if limit is None:
                    limit = 1000
                else:
                    limit = int(limit)
                start_page = page * limit - limit
                end_page = page * limit
                res['data'] = svc_list[start_page: end_page]
                sus['data'] = res
            except Exception as e:
                print(e)
                sus['code'] = 500
            return JsonResponse(sus)

    @method_decorator(login_required)
    def post(self, request, types):
        if types == 'delete':
            ret = {'code': 0}
            ns = request.POST.get('ns')
            svc_name = request.POST.get('name')
            print(svc_name, ns)
            try:
                config.load_kube_config()
                api_instance = client.CoreV1Api()
                body = client.V1DeleteOptions()
                api_instance.delete_namespaced_service(name=svc_name, namespace=ns, body=body)
            except ApiException as e:
                tmp = eval(str(e.body))
                ret['code'] = tmp.get('code')
                ret['msg'] = tmp.get('message')
            return JsonResponse(ret, safe=True)
        if types == 'add':
            ret = dict()
            ret["code"] = 0
            ns = request.POST.get('ns')
            labels = request.POST.get('selector')
            name = request.POST.get('name', labels)
            ports = int(request.POST.get('source_port'))
            target = int(request.POST.get('target_port'))
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
                ret['msg'] = "add success!"
            except ApiException as e:
                tmp = eval(str(e.body))
                ret['code'] = tmp.get('code')
                ret['msg'] = tmp.get('message')
            return JsonResponse(ret, safe=True)

        return JsonResponse({"code": 404})
