__author__ = 'charlie'

from sinaapi.fetch.util import BaseFetcher





class SingleUserFetcher(BaseFetcher):

    def __init__(self, **kwargs):
        BaseFetcher.__init__(self, **kwargs)

    def fetch(self):
        return BaseFetcher.fetch(self)

    class Meta:
        param_names = ['uid', 'screen_name']
        role = 'user'
        method = 'get_one'



