__author__ = 'charlie'

from django.conf.urls import patterns, url

urlpatterns = patterns('ne.views',

    url(r'^test$', 'test_view'),

)
