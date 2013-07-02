from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.db.models import Q

from network.models import (
    SNUserRelation,
    SNUser,
    Status,
    )

from shared.util import set_value

import operator


# Create your views here.

def sns_visualization_view(request):

    return render_to_response("sns-visual.html")

def control_panel_view(request):

    return render_to_response("ner/control-panel.html")

def conditional_recognize_view(request):

    return render_to_response("ner/condition_recognize.html")


def get_all_relations_view(request):

    return HttpResponse(content=serializers.serialize('json', SNUserRelation.objects.all()), mimetype='application/json')


def get_user_operation_snippet_view(request):

    uid = request.GET['uid']

    user = SNUser.objects.get(id=uid)

    template = get_template('snippets/user-operation-snippet.html')

    context = Context({'user':user})

    rendered = template.render(context)

    return HttpResponse(rendered)


def get_statuses_view(request):

    # import pdb;pdb.set_trace()


    pageNo = set_value('page', request.GET, 1)
    count = set_value('count', request.GET, 10)

    # query the statues by user id
    if 'uid' in request.GET:
        uid = request.GET['uid']

        statusQuerySet = Status.objects.filter(user__idstr=uid)

        paginator = Paginator(statusQuerySet, count)

        try:
            statuses = paginator.page(int(pageNo))
        except PageNotAnInteger:
            statuses = paginator.page(1)
        except EmptyPage:
            statuses = paginator.page(paginator.num_pages)

        template = get_template('snippets/status/statuses-visual-modal-snippet.html')

        context = Context({'statuses': statuses, 'uid': uid})

        rendered = template.render(context)

        return HttpResponse(rendered)


    # query statuses by keywords
    else:

        # TODO: other condition

        if 'keyword' in request.GET:


            keywordStr = request.GET['keyword']

            keywords = keywordStr.split(',')


            keywordCond = [Q(text__icontains=w) for w in keywords]



            # import pdb;pdb.set_trace()

            if "exclude" in request.GET:
                excludeIDsStr = request.GET["exclude"]
                excludeIDs = excludeIDsStr.split(',')

                excludeCond = [Q(user__idstr=id) for id in excludeIDs]

                statusQuerySet = Status.objects.filter(reduce(operator.or_, keywordCond)).exclude(reduce(operator.or_, excludeCond))
            else:
                statusQuerySet = Status.objects.filter(reduce(operator.or_, keywordCond))

            idsStr = str()

            for s in statusQuerySet:
                idsStr += s.idstr + ','
            idsStr = idsStr[:-1]

            paginator = Paginator(statusQuerySet, count)

            try:
                statuses = paginator.page(int(pageNo))
            except PageNotAnInteger:
                statuses = paginator.page(1)
            except EmptyPage:
                statuses = paginator.page(paginator.num_pages)

            template = get_template('snippets/status/statuses-control-panel-snippet.html')

            context = Context({'statuses': statuses, 'keywordStr': keywordStr, 'ids': idsStr})

            rendered = template.render(context)

            return HttpResponse(rendered)

