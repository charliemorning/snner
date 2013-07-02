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



import CRFPP

from feature import create_tags

tagger = None


def test(input, tags):

    global tagger

    if tagger is None:

        print input
        tagger = CRFPP.Tagger(str(input))



    tagger.clear()

    # tags = create_tags(data)

    for tag in tags:

        tagger.add(tag.encode('UTF-8'))

    tagger.parse()

    size = tagger.size()
    ysize = tagger.ysize()

    result = []

    for i in xrange(size):

        word = tagger.x(i, 0)

        cates = []

        # to iterate each tag
        for j in xrange(ysize):
            p = tagger.prob(i, j)
            alpha = tagger.alpha(i, j)
            beta = tagger.beta(i, j)

            cate = tagger.yname(j)

            cates.append((cate, p, alpha, beta,))

        idx =tagger.y(i)
        best = (tagger.y2(i), tagger.prob(i, idx), tagger.alpha(i, idx), tagger.beta(i, idx),)

        result.append((word, best, cates,))



    return result


