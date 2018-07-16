from django.conf.urls import url, include
from .node import NodeOperating

urlpatterns = [
    url('^', include([
        # url('^pod/$', pod.PodList.as_view()),
        url(r'^node/(?P<types>.*)$', NodeOperating.as_view(), name="operating"),
    ]))
]
