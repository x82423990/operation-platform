from django.conf.urls import url, include
from . import views
from . import pod, deployment, service, ingress, namespaces, image
urlpatterns = [
    # url('^$', views.IndexView.as_view()),
    url('^k8s/', include([
        url('^pod/$', pod.PodList.as_view()),
        # url('^test/$', views.Test.as_view()),
        url('dp/$', deployment.DpList.as_view(), name="DpList"),
        # url('ns/$', ns.NsList.as_view(), name="NsList"),
        url(r'^dp/(?P<types>.*)$', deployment.DpManagement.as_view(), name='DpManagement'),
        url(r'^select/(?P<types>.*)', deployment.SelectType.as_view()),
        url(r'^nmlist/$', namespaces.Nm_list.as_view()),
        url(r'^nmlist/(?P<types>.*)', namespaces.Nm_list.as_view()),
        url(r'^image/(?P<types>.*)', image.Image.as_view(), name='images'),

        # url(r'^delete/ns/(?P<ns>.*)/$', deletes.delete_ns, name='delete'),
        # url(r'^dp/$', k8s.Dp_list.as_view(), name='test'),
        # url(r'^select/(?P<types>.*)', k8s.SelectType.as_view(), name='ls_ns'),
        # url(r'^svc/$', k8s.Svc_list.as_view(), name='list_svc'),
        url(r'^svc/(?P<types>.*)$', service.SvcManagement.as_view()),
        url(r'^ing/(?P<types>.*)$', ingress.IngressManagement.as_view(), name='m_c_ing'),
        # url(r'^test/$', k8s.pr_test.as_view()),
    ]))
]
