'''
#=============================================================================
#     FileName: test.py
#         Desc:
#       Author: Charlie
#        Email: zhangchen143@gmail.com
#     HomePage: http://blog-charliemorning.rhcloud.com
#      Version: 0.0.1
#   LastChange: 2013-03-15 20:53:11
#      History:
#=============================================================================
'''
# -*- coding: UTF-8 -*-

import os
import codecs

import CRFPP

from feature import create_tags
from ne.recognition.data import (
        process_url,
        process_at_person
    )

tagger = None

def test(config, data):

    global tagger

    if tagger is None:

        input = '-m %s -v 3 -n2'%(config['model'])
        print input
        tagger = CRFPP.Tagger(str(input))



    tagger.clear()


    tags = create_tags(data)

    for tag in tags:

        #import pdb;pdb.set_trace()

        tagger.add(tag.encode('UTF-8'))

    tagger.parse()

    size = tagger.size()
    ysize = tagger.ysize()

    result = []

    for i in xrange(size):

        word = tagger.x(i, 0)

        cates = []

        for j in xrange(ysize):
            p = tagger.prob(i, j)
            alpha = tagger.prob(i, j)
            beta = tagger.prob(i, j)

            cate = tagger.yname(j)

            cates.append((cate, p, alpha, beta,))

        result.append((word, cates,))

    return result


