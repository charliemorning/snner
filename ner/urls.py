__author__ = 'charlie'

from django.conf.urls import patterns, url

urlpatterns = patterns('ner.views',

    url(r'^recognize$', 'recognize_entity_view'),
    url(r'^entity$', 'get_entity_view'),

    url(r'^test$', 'test_view1'),

)
