from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from kubernetes import client, config
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator

class PodList(View):
    @method_decorator(login_required)
    def get(self, request):
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        config.load_kube_config()
        v1 = client.CoreV1Api()
        latest_question_list = v1.list_pod_for_all_namespaces(watch=False)
        count = 1
        res = dict()
        tmp = []
        res['code'] = 0
        res['data'] = []

        for i in latest_question_list.items:
            ret = dict()
            ret["ip"] = i.status.pod_ip
            ret["phase"] = i.status.phase
            ret["name"] = i.metadata.name
            tmp.append(ret)
            count += 1
        res['count'] = count
        if page == 1:
            startPage = 0
            endPage = startPage + limit
        else:
            startPage = page * limit - limit
            endPage = startPage + limit
        print(startPage, endPage)
        res['data'] = tmp[startPage:endPage]

        return JsonResponse(res, safe=True)
