__author__ = 'charlie'

from django.conf.urls import patterns, url, include




urlpatterns = patterns('network.views',


    # page
    url(r'^visual$', 'sns_visualization_view'),
    url(r'^control$', 'control_panel_view'),
    url(r'^cond$', 'conditional_recognize_view'),

	url(r'^getall$', 'get_all_relations_view'),
	url(r'^user/optsnippet$', 'get_user_operation_snippet_view'),
	url(r'^status/show$', 'get_statuses_view'),


)
