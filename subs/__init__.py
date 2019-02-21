from django.views.generic import View

from django.http import JsonResponse

# from subs import producter
from sendmail import Mail


class Sub(View):
    def post(self, request, types):
        data = request.POST.get('data', None)
        tatil = '''各位好:\n本次发布内容为\n项目      镜像                tag\n'''
        for i in eval(data):
            print(i.get('tag'))
            print(i.get('image'))
            context = i.get('project') + "   " + i.get("image") + "   " + i.get('tag') + "\n"
            tatil += context
        m = Mail(content=tatil)
        if m.send():
            return JsonResponse({"code": 0})
        else:
            return JsonResponse({"code": 4})
