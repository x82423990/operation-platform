from django.views.generic import TemplateView, View
from kubernetes import client, config
import time, random, string
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from kubernetes.client.rest import ApiException
from .DpApi import create_deployment, create_deployment_object, delete_deployment, update_deployment
from k8s import hub as repitl


class SelectType(View):

    def get(self, request, types):
        # if types == 'add':
        #     return render(request, 'seconds/add.html', {'title': 'add dep'})
        if types == 'img':
            a = repitl.get_image_name()
            return JsonResponse(a, safe=False)

        if types == 'pj':
            print(repitl.get_project())

            return JsonResponse(repitl.get_project())

        if types == 'ns':
            config.load_kube_config()
            v1 = client.CoreV1Api()
            nm_list = []
            for i in v1.list_namespace(watch=False).items:
                nm_list.append(i.metadata.self_link.split('/')[-1])
            return JsonResponse(nm_list, safe=False)

    def post(self, request, types):
        if types == 'img':
            pj_id = request.POST.get('pid', None)
            print(pj_id)
            a = repitl.get_image_name(project_id=pj_id)
            print(a)
            return JsonResponse(a, safe=False)

        if types == 'tags':
            repo_name = request.POST.get('image')
            tags = repitl.get_tags(repo_name)
            print('tags:', tags)

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
            print(ns)
            config.load_kube_config()
            v1 = client.CoreV1Api()
            ret = []
            tmp = v1.list_namespaced_service(ns).items
            for i in tmp:
                ret.append(i.metadata.name)
            return JsonResponse(ret, safe=False)


class DpManagement(View):

    def post(self, request, types):
        ret = {'code': 0}
        if types == 'add':
            salt = '-' + ''.join(random.sample(string.ascii_lowercase, 4))
            ns = request.POST.get('ns')
            msg = request.POST.get('image')
            tags = request.POST.get('tags')
            rc = int(request.POST.get('rc'))
            env = request.POST.get('env')
            print(salt, ns, msg, tags, rc, env)
            # if not request.POST.get('dp_name', None):
            #     dp_name = msg.split('/')[-1] + salt
            # else:
            #     dp_name = request.POST.get('dp_name', None) + salt
            #
            # print(ns, msg, tags, rc, env)
            # config.load_kube_config()
            # extensions_v1beta1 = client.ExtensionsV1beta1Api()
            # try:
            #     deploy = create_deployment_object(tags=tags, images=msg, rc=rc, envs=env, name=dp_name)
            #     create_deployment(extensions_v1beta1, deploy, ns=ns)
            # except ApiException as e:
            #     tmp = eval(str(e.body))
            #     ret['code'] = tmp.get('code')
            #     ret['msg'] = tmp.get('message')
            return JsonResponse(ret, safe=True)

        if types == 'delete':
            ns = request.POST.get('ns_name')
            dp_name = request.POST.get('dp_name')
            print(ns, dp_name)
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
                    ret['msg'] = 'ok'
                except Exception as e:
                    ret['code'] = 55
                    ret['msg'] = e
                return JsonResponse(ret)

        if types == 'update':
            ret = {'code': 0}
            dp_name = request.POST.get('dp_name')
            env = request.POST.get('config')
            img = request.POST.get('image')
            ns = request.POST.get('ns')
            tags = request.POST.get('pp')
            rc = request.POST.get('rc')
            print(dp_name, env, img, tags, ns, rc)
            ret['mgs'] = 'ok'
            # config.load_kube_config()
            # api = client.ExtensionsV1beta1Api()
            # try:
            #     dp_obj = api.read_namespaced_deployment(name=dp_name, namespace=ns)
            #     # get dep obj
            #     deployment = client.ExtensionsV1beta1Deployment(
            #         api_version="extensions/v1beta1",
            #         kind="Deployment",
            #         metadata=client.V1ObjectMeta(name=dp_obj.metadata.name),
            #         spec=dp_obj.spec)
            #     # get env
            #     tmp = eval(str(deployment.spec.template.spec.containers[0].env[0]))
            #     tmp['value'] = env
            #     images = 'hub.cbble.com/' + img + ':' + tags
            #     deployment.spec.template.spec.containers[0].image = images
            #     deployment.spec.replicas = int(rc)
            #     deployment.spec.template.spec.containers[0].env[0] = tmp
            #
            #     api.patch_namespaced_deployment(
            #         name=dp_obj.metadata.name,
            #         namespace=ns,
            #         body=deployment)
            #
            # except ApiException as e:
            #
            #     tmp = eval(str(e.body))
            #
            #     ret['code'] = tmp.get('code')
            #
            #     ret['msg'] = tmp.get('message')

            return JsonResponse(ret, safe=True)
