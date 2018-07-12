from django.views.generic import View
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator


class IngressManagement(View):

    @method_decorator(login_required)
    def get(self, request, types):
        configuration = config.load_kube_config()
        api_instance = client.ExtensionsV1beta1Api(client.ApiClient(configuration))
        if types == "list":
            try:
                page = int(request.GET.get('page', 1))
                limit = request.GET.get('limit', 1000)
                keyword = request.GET.get('keyword')
                ns = request.GET.get('ns')
                test = request.GET.get('test', 0)
            except TypeError:
                return JsonResponse({'code': 501, "msg": "Wrong or miss parameters!"})
            res = dict()
            sus = dict()
            ret = []
            count = 0
            if ns:
                tmp = api_instance.list_namespaced_ingress(ns).items
            else:
                tmp = api_instance.list_ingress_for_all_namespaces().items
            try:
                for i in tmp:
                    tmp = {'name': i.metadata.name, 'namespaces': i.metadata.namespace,
                           'svc_name': i.spec.rules[0].http.paths[0].backend.service_name,
                           'svc_port': i.spec.rules[0].http.paths[0].backend.service_port,
                           'host': i.spec.rules[0].host}
                    if keyword:
                        if keyword in tmp.get("name"):
                            ret.append(tmp)
                            count += 1
                    else:
                        ret.append(tmp)
                        count += 1
                res['count'] = count
                sus["code"] = test
                if limit is None:
                    limit = 10000
                start_page = page * limit - limit
                end_page = page * limit
                res['data'] = ret[start_page: end_page]
                sus['data'] = res
            except ApiException as e:
                sus['code'] = 500
                sus['msg'] = e.status
            return JsonResponse(sus, safe=False)
        return JsonResponse({"code": 404})

    @method_decorator(login_required)
    def post(self, request, types):
        if types == "add":
            ret = {'code': 0}
            ns = request.POST.get('ns')
            svc_name = request.POST.get('selector')
            svc_port = request.POST.get('target_port', 80)
            ing_name = request.POST.get('name', svc_name)
            config.load_kube_config()
            body = client.V1beta1Ingress()
            body.api_version = 'extensions/v1beta1'
            body.kind = 'Ingress'
            bakend = client.V1beta1IngressBackend(service_name=svc_name, service_port=int(svc_port))
            paths = [client.V1beta1HTTPIngressPath(backend=bakend)]

            htp = client.V1beta1HTTPIngressRuleValue(paths=paths)
            rules = [client.V1beta1IngressRule(host=ing_name + '.test.cbble.com', http=htp)]

            body.metadata = client.V1ObjectMeta(name=ing_name)
            body.spec = client.V1beta1IngressSpec(rules=rules)
            api = client.ExtensionsV1beta1Api()
            try:
                api.create_namespaced_ingress(namespace=ns, body=body)

            except ApiException as e:
                tmp = eval(str(e.body))
                ret['status'] = tmp.get('code')
                ret['msg'] = tmp.get('message')
                return JsonResponse(ret)
            except ValueError:
                return JsonResponse({"code": 477, "msg": "Params Err"})
            return JsonResponse(ret, safe=True)

        if types == 'delete':

            ret = {'status': 0}
            ing_name = request.POST.get('name')
            ns = request.POST.get('ns')
            config.load_kube_config()
            try:
                ad = client.V1DeleteOptions(api_version='extensions/v1beta1')
                client.ExtensionsV1beta1Api().delete_namespaced_ingress(namespace=ns, name=ing_name, body=ad)
            except ApiException as e:
                print("Exception when calling ExtensionsV1beta1Api->create_namespaced_ingress: %s\n" % e)
                ret['status'] = 12
                ret['msg'] = e
                return JsonResponse(ret, safe=True)
            return JsonResponse(ret, safe=True)

        if types == 'update':
            ret = {'status': 0}
            ing_name = request.POST.get('ing_name', None)
            m_ns = request.POST.get('m_ns', None)
            m_port = request.POST.get('m_port', None)
            m_host = request.POST.get('m_host', None)
            m_label = request.POST.get('m_label', None)
            config.load_kube_config()
            api = client.ExtensionsV1beta1Api()
            try:
                ing_obj = api.read_namespaced_ingress(ing_name, m_ns)
                ing_obj.spec.rules[0].http.paths[0].backend.service_name = m_label
                ing_obj.spec.rules[0].http.paths[0].backend.service_port = int(m_port)
                ing_obj.spec.rules[0].host = m_host
                api.patch_namespaced_ingress(ing_name, m_ns, ing_obj)
                ret['msg'] = 'succeed'
            except ApiException as e:
                tmp = eval(str(e.body))
                ret['status'] = tmp.get('code')
                ret['msg'] = tmp.get('message')
            return JsonResponse(ret, safe=True)

        return JsonResponse({"code": 404})
