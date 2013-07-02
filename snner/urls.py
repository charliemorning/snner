from django.conf.urls import patterns, include, url


from sinaapi.urls import urlpatterns as sinaapi_urlpatterns
from network.urls import urlpatterns as network_urlpatterns
from ner.urls import urlpatterns as ner_urlpatterns






from django.contrib import admin
admin.autodiscover()





urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^sinaapi/', include(sinaapi_urlpatterns)),
    url(r'^network/', include(network_urlpatterns)),
    url(r'^ner/', include(ner_urlpatterns)),
)
