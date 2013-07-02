__author__ = 'charlie'

from sinaapi.fetch.util import BaseFetcher

class ActiveFansFetcher(BaseFetcher):

    def __init__(self, **kwargs):

        BaseFetcher.__init__(self, **kwargs)

    class Meta:

        param_names = ['uid', 'count']
        role = 'relation'
        method = 'active_fans'
