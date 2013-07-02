__author__ = 'charlie'

from django.conf.urls import patterns, url, include
from rest_framework import routers
from sinaapi import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = patterns('sinaapi.views',

    url(r'^', include(router.urls)),
    url(r'^init$', 'get_init_page_view'),
    url(r'^net$', 'get_network_view'),
	url(r'^new$', 'get_request_log_view'),
    url(r'^user/get$', 'get_single_user_view'),
    url(r'^relation/fans/active$', 'get_active_fans_view'),
    url(r'^status/getall$', 'get_all_status_view'),
    url(r'^status/cond$', 'get_conditional_status_request_page_view'),
    url(r'^status/cond_form$', 'conditional_status_request_view'), # reply the form

)
