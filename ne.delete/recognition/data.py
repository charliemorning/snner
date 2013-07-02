'''
#=============================================================================
#	 FileName: data.py
#		 Desc:
#	   Author: Charlie
#		Email: zhangchen143@gmail.com
#	 HomePage: http://blog-charliemorning.rhcloud.com
#	  Version: 0.0.1
#   LastChange: 2013-01-12 19:41:11
#	  History:
#=============================================================================
'''

# -*- coding: UTF-8 -*-

__author__ = 'Charlie'

import re
import json
import os
import codecs

def load_config():

    try:

        root = os.path.dirname(globals()["__file__"])

        f = codecs.open(os.path.join(root, 'config.json'), 'r', 'UTF-8')
        config_text = f.read()
        f.close()


        root = re.sub(ur'\\', '/', root)

        config_text = re.sub(ur"%root%", root, config_text)

        config = json.loads(config_text)

    except:
        print "fail to load config.json."
        raise

    return config


AT_PATTERN = re.compile(ur'@\W+')
SHORT_URL_PATTERN = re.compile(ur'https://t.com\w+')

AT_REPL = 'ATTAG'
SHORT_URL_REPL = 'HTTPURL'

def process_at_person(t):
    return re.sub(AT_PATTERN, AT_REPL, t)

def process_url(t):
    return re.sub(SHORT_URL_PATTERN, SHORT_URL_REPL, t)


def read_raw_weibo_input_into_memory(fn):
    """"
    this method allow to load weibos in a file as each one as a line
    """

    weibos = []

    f = codecs.open(fn, 'r', 'UTF-8')

    for line in f:
        weibos.append(line)
    f.close()

    return weibos



def xml2bio(s, **kwargs):
    '''
    Generate BIO-token pairs from xml-style annotation.
    Notes:
      1) All white space including space and tab will be ignored.
      2) Assumes no self-closing tags
      3) Assumes no nesting

    >>> x = xml2bio("<title>Cat in the Hat</title><author>Dr. Seuss</author>")
    >>> list(x)                                  #doctest:+NORMALIZE_WHITESPACE
    [('B-title', 'Cat'), ('I-title', 'in'), ('I-title', 'the'),
     ('I-title', 'Hat'), ('B-author', 'Dr.'), ('I-author', 'Seuss')]
    '''

    #p = ur'(?:(?:<([A-Za-z0-9]+)>\s*([\w\W%]+?)\s*</(\1)>)|([\u4e00-\u9fa5]+?|[\w%]+))'
    p = ur'(?:(?:<([A-Za-z0-9]+)\s*type="(\w+)">\s*([\w\W]+?)\s*</(\1)>)|([\u4e00-\u9fa5]+?|[\w]+|%))'

    for label, tp, tagged, close, word in re.findall(p, s):
        #assert close != label, 'Mismatched xml tags (%s, %s)' % (close, label)
        if word:
            yield (word, u'N')
        else:
            words = iter(re.findall(ur'([\u4e00-\u9fa5]|[\w]+)', tagged))

            cate = u'%s' % (label)

            yield (words.next(), u'B-%s'%cate)
            for w in words:
                yield (w, u'I-%s'%cate)

# print [e for e in xml2bio(u'thi is a test 23%')]
