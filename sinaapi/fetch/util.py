__author__ = 'charlie'

import urllib

import httplib2

import json
import time

from sinaapi.fetch.error import is_error, check_error

from sinaapi.fetch.shared import config


def filter_param(set, pns):

    param = dict()

    for pn in pns:
        if pn in set:
            param.update({pn:set[pn]})

    return param


def make_simple_request(url, param, callback=None):

    data = urllib.urlencode(param)

    url = '%s?%s' % (url, data)

    http = httplib2.Http(timeout=10)

    print url

    try:
        resp, content = http.request(url, 'GET')
    except:
        raise

    return url, resp, content


class BaseFetcher:

    Config = config

    def __init__(self, **kwargs):

        self.param = filter_param(kwargs, self.Meta.param_names)
        self.param.update({u'access_token': self.Config['access_token']})

    def fetch(self):

        url, resp, content = make_simple_request(self.Config[self.Meta.role][self.Meta.method], self.param)

        jsonObj = json.loads(content)

        if is_error(jsonObj):

            code, desc = check_error(jsonObj)

            print code, desc

            if int(code) in [10022, 10023]:

                sec = 100

                print "sleep %d secs." % sec
                time.sleep(sec)

                return self.fetch()

        return url, resp, content