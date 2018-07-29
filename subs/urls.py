from django.conf.urls import url, include
from subs import Sub

urlpatterns = [
    url('^', include([
        # url('^pod/$', pod.PodList.as_view()),
        url(r'^sendmail/(?P<types>.*)$', Sub.as_view(), name="operating"),
        # url(r'^monitor/(?P<types>.*)$', Monitor.as_view(), name="monitor"),
    ]))
]
