from django.views.generic import View
from kubernetes import client, config
import time
from django.http import JsonResponse
from kubernetes.client.rest import ApiException
from .DpApi import create_deployment, create_deployment_object, delete_deployment, update_deployment
from k8s import hub as repitl
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator
from datetime import timedelta, timezone


class DpList(View):
    # @method_decorator(login_required)
    def get(self, request):
        # a = json.loads(request.body)
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        print(page)
        namespace = request.GET.get('namespace')
        keyword = request.GET.get('keyword')
        config.load_kube_config()
        v1 = client.AppsV1Api()
        res = dict()
        suc = dict()
        count = 0
        dp_list = []
        if namespace:
            tmp = v1.list_namespaced_deployment(namespace=namespace).items
        else:
            tmp = v1.list_deployment_for_all_namespaces().items
        try:
            for i in tmp:
                ret = dict()
                timeP = i.metadata.creation_timestamp.replace(tzinfo=timezone.utc).astimezone(
                    timezone(timedelta(hours=8)))
                times = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.mktime(
                    timeP.timetuple())))
                uptimeP = i.status.conditions[1].last_update_time.replace(tzinfo=timezone.utc).astimezone(
                    timezone(timedelta(hours=8)))
                uptimes = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.mktime(
                    uptimeP.timetuple())))
                ret['name'] = i.metadata.name
                ret['ns'] = i.metadata.namespace
                ret['replicas'] = i.status.replicas
                ret['available_replicas'] = i.status.available_replicas
                ret['create_time'] = times
                ret['update_time'] = uptimes
                for j in i.spec.template.spec.containers:
                    ret['project'] = j.image.split('/')[1]
                    # ret['pid'] = repitl.get_project_id(ret['project'])
                    tmp_image = j.image.split('/')[-1]
                    ret['image'] = tmp_image.split(":")[0]
                    tag_list = tmp_image.split(":")
                    if len(tag_list) > 1:
                        ret["tag"] = tag_list[1]
                    else:
                        ret["tag"] = "latest"
                    if not j.env:
                        ret['env'] = 'no config'
                    else:
                        ret['env'] = j.env[0].value
                if keyword:
                    if keyword in ret.get("name"):
                        dp_list.append(ret)
                else:
                    dp_list.append(ret)

                count += 1
            suc['code'] = 0
            res['count'] = count
        except Exception as e:
            print(e)
            suc['code'] = 6
            res['count'] = 0
            res['data'] = e
        if limit is None:
            limit = 10000
        page = int(page)
        limit = int(limit)
        startPage = page * limit - limit
        endPage = startPage + limit
        data = dp_list[startPage:endPage]
        data.sort(key=lambda x: x["update_time"], reverse=True)
        res['data'] = data
        suc['data'] = res
        return JsonResponse(suc, safe=True)


class SelectType(View):
    # @method_decorator(login_required)
    def get(self, request, types):

        if types == 'img':
            a = repitl.get_image_name()
            return JsonResponse(a, safe=False)

        if types == 'pj':
            return JsonResponse(repitl.get_project())

        if types == 'ns':
            config.load_kube_config()
            v1 = client.CoreV1Api()
            nm_list = []
            for i in v1.list_namespace(watch=False).items:
                nm_list.append(i.metadata.self_link.split('/')[-1])
            return JsonResponse(nm_list, safe=False)

        if types == 'all':
            ret = repitl.get_all()

            return JsonResponse(ret, safe=True)

    # @method_decorator(login_required)
    def post(self, request, types):
        if types == 'img':
            ret = dict()
            ret["code"] = 0
            try:
                pj_id = request.POST.get('pid', None)
                a = repitl.get_image_name(project_id=pj_id)
            except Exception as e:
                ret["code"] = 2

            return JsonResponse(a, safe=False)

        if types == 'tags':
            repo_name = request.POST.get('image')
            tags = repitl.get_tags(repo_name)

            return JsonResponse(tags, safe=False)

        if types == 'dep':
            ns = request.POST.get('ns')
            config.load_kube_config()
            v1 = client.AppsV1beta2Api()
            ret = []
            tmp = v1.list_namespaced_deployment(namespace=ns).items
            for i in tmp:
                ret.append(i.metadata.name)
            return JsonResponse(ret, safe=False)

        if types == 'svc':
            ns = request.POST.get('ns')
            config.load_kube_config()
            v1 = client.CoreV1Api()
            ret = []
            tmp = v1.list_namespaced_service(ns).items
            for i in tmp:
                ret.append(i.metadata.name)
            return JsonResponse(ret, safe=False)


class DpManagement(View):
    # @method_decorator(login_required)
    def post(self, request, types):
        ret = dict()
        ret['code'] = 0
        ret["msg"] = "sucess"
        if types == 'add':
            # salt = '-' + ''.join(random.sample(string.ascii_lowercase, 4))
            ns = request.POST.get('ns')
            msg = request.POST.get('image')
            tags = request.POST.get('tag')
            rc = request.POST.get('rc')
            env = request.POST.get('env')
            dp_name = request.POST.get('name', None)
            if not dp_name:
                dp_name = msg.split('/')[-1]
            config.load_kube_config()
            extensions_v1beta1 = client.ExtensionsV1beta1Api()
            try:
                deploy = create_deployment_object(tags=tags, images=msg, rc=int(rc), envs=env, name=dp_name)
                create_deployment(extensions_v1beta1, deploy, ns=ns)
            except ApiException as e:
                tmp = eval(str(e.body))
                ret['code'] = tmp.get('code')
                ret['msg'] = tmp.get('message')
            return JsonResponse(ret, safe=True)
        if types == 'delete':
            ns = request.POST.get('ns')
            dp_name = request.POST.get('name')
            ret = {'code': 0}
            if dp_name is None:
                ret['code'] = 100
                ret['msg'] = 'ns_name or dp_name is None'
                return JsonResponse(ret)
            else:
                try:
                    config.load_kube_config()
                    extensions_v1beta1 = client.ExtensionsV1beta1Api()
                    delete_deployment(extensions_v1beta1, ns=ns, images=dp_name)
                    ret['code'] = 0
                    ret['msg'] = '删除成功'
                except ApiException as e:
                    tmp = eval(str(e.body))
                    ret['code'] = tmp.get('code')
                    ret['msg'] = tmp.get('message')
            return JsonResponse(ret)
        if types == 'update':
            ret = {'code': 0}
            dp_name = request.POST.get('name')
            env = request.POST.get('env')
            img = request.POST.get('image')
            ns = request.POST.get('ns')
            # pj = request.POST.get('project')
            tags = request.POST.get('tag')
            rc = request.POST.get('rc')
            config.load_kube_config()
            api = client.ExtensionsV1beta1Api()
            print("getname", dp_name, rc)
            try:
                dp_obj = api.read_namespaced_deployment(name=dp_name, namespace=ns)
                # get dep obj
                deployment = client.ExtensionsV1beta1Deployment(
                    api_version="extensions/v1beta1",
                    kind="Deployment",
                    metadata=client.V1ObjectMeta(name=dp_obj.metadata.name),
                    spec=dp_obj.spec)
                # get env
                tmp = eval(str(deployment.spec.template.spec.containers[0].env[0]))
                tmp['value'] = env
                images = 'hub.cbble.com/' + img + ':' + tags
                print(images)
                deployment.spec.template.spec.containers[0].image = images
                deployment.spec.replicas = int(rc)
                deployment.spec.template.spec.containers[0].env[0] = tmp
                api.patch_namespaced_deployment(
                    name=dp_obj.metadata.name,
                    namespace=ns,
                    body=deployment)

            except ApiException as e:

                tmp = eval(str(e.body))

                ret['code'] = tmp.get('code')

                ret['msg'] = tmp.get('message')

            return JsonResponse(ret, safe=True)
