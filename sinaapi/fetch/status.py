__author__ = 'charlie'



from sinaapi.fetch.util import BaseFetcher


class StatusFetcher(BaseFetcher):

    def __init__(self, **kwargs):
        BaseFetcher.__init__(self, **kwargs)

    def fetch(self):
        return BaseFetcher.fetch(self)

    class Meta:
        param_names = ['uid', 'screen_name', 'since_id', 'max_id', 'count', 'page', 'base_app', 'feature', 'trim_user']
        role = 'status'
        method = 'get'
