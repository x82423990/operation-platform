from django.conf.urls import url, include
from .node import NodeOperating, Monitor

urlpatterns = [
    url('^', include([
        # url('^pod/$', pod.PodList.as_view()),
        url(r'^node/(?P<types>.*)$', NodeOperating.as_view(), name="operating"),
        url(r'^monitor/(?P<types>.*)$', Monitor.as_view(), name="monitor"),
    ]))
]
