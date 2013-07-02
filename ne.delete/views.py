from django.shortcuts import render
from django.http import HttpResponse


import threading
import json

# from network.models import Status

from ne.recognition.test import (
    test,
    )
from ner.recognition.data import (
    load_config,
    process_at_person,
    process_url,
    )
#
#
#
# class StartTestTask(threading.Thread):
#
#     def __init__(self, uid):
#
#         threading.Thread.__init__(self)
#         self.uid = uid
#         self.config = load_config()
#
#     def run(self):
#         """
#         """
#
#         # to get the pieces of specific user
#         statuses = Status.objects.filter(user__idstr=self.uid)
#
#         for status in statuses:
#
#
#             # preprocess
#             text = status.text
#             text = process_at_person(text)
#             text = process_url(text)
#             result = test(self.config, text)
#
#             # for one piece of weibo
#
#             pos = 0
#             for token in result:
#
#                 # current word
#                 word = token[0]
#
#                 # the all possible categories of current token
#                 cates = token[1]
#
#
#                 # to get the first token, which is the most likely category
#                 it = iter(cates)
#                 most = it.next()
#
#                 # unzip the element
#                 cate, p, alpha, beta = most
#
#
#                 # entity = Entity()
#                 # entity.save_entity(status, cate=cate, p=p, alpha=alpha, beta=beta, content=word, text='', pos=pos)
#                 #
#                 # for other in it:
#                 #
#                 #     cand = Candidate()
#                 #
#                 #     cate, p, alpha, beta = other
#                 #
#                 #     cand.save_candidate(entity, cate=cate, p=p, alpha=alpha, beta=beta)
#                 #
#                 # pos += 1
#         print 'done'
#
#
#
#
#
#
#
#










def test_view(request):
    return HttpResponse('asdf')



