from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.response import TemplateResponse

# from django.template import RequestContext
# from django.core.context_processors import csrf
# from django.core import serializers

from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone

from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from sinaapi.serializers import UserSerializer, GroupSerializer

import threading
import json
import time
import datetime

from sinaapi.fetch.user import SingleUserFetcher
from sinaapi.fetch.relation import ActiveFansFetcher
from sinaapi.fetch.status import StatusFetcher
from sinaapi.fetch.error import is_error, check_error
from sinaapi.fetch.shared import network_target_ids

from network.models import (
    SNUser,
    SNUserRelation,
    Status,
    )

from sinaapi.models import Record

from sinaapi.forms import ConditionalStatusRequestForm

from shared.util import set_value


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


########################################################################################################################


class BaseTask(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)


class FetchSingleUserTask(BaseTask):

    def __init__(self, uid):

        BaseTask.__init__(self)

        self.uid = uid

    def run(self):

        url, resp, text = SingleUserFetcher(uid=self.uid).fetch()

        rec = Record(url=url, date=datetime.datetime.now(), result_code=resp['status'], info='')
        rec.save()

        jsonObj = json.loads(text)

        if is_error(jsonObj):
            code, desc = check_error(jsonObj)
            print code, desc
        else:
            user = SNUser()
            user.save_str(text)

        print 'done'


class FetchUserActiveFansTask(BaseTask):

    def __init__(self, uid):

        BaseTask.__init__(self)

        self.uid = uid

    def run(self):

        try:
            url, resp, text = ActiveFansFetcher(uid=self.uid).fetch()
            rec = Record(url=url, date=datetime.datetime.now(), result_code=resp['status'], info='')
            rec.save()
        except:
            raise

        jsonObj = json.loads(text)

        if is_error(jsonObj):

            code, desc = check_error(jsonObj)

            print code, desc

            return

        for user in jsonObj['users']:

            u = SNUser()

            u.save_obj(user)

            relation = SNUserRelation()

            u1 = SNUser.objects.get(idstr=self.uid)
            u2 = SNUser.objects.get(idstr=u.idstr)

            relation.follower = u1
            relation.followee = u2

            relation.save()
        print 'done'


class FetchNetworkTask(BaseTask):

    def __init__(self, **option):

        BaseTask.__init__(self)

        self.option = option

        self.maxDepth = set_value("d", option, 2)

    def getNetwork(self, id, depth):

        if depth <= 0:
            print "max depth!"
            return

        try:
            url, resp, text = ActiveFansFetcher(uid=id).fetch()
            rec = Record(url=url, date=datetime.datetime.now(), result_code=resp['status'], info='')
            rec.save()
        except:
            raise

        jsonObj = json.loads(text)

        if is_error(jsonObj):

            code, desc = check_error(jsonObj)

            print code, desc

            return

        userList = list()

        for user in jsonObj['users']:

            u = SNUser()

            u.save_obj(user)

            relation = SNUserRelation()

            try:

                u1 = SNUser.objects.get(idstr=id)
                u2 = SNUser.objects.get(idstr=u.idstr)
            except:
                print "error"
                continue

            relation.follower = u1
            relation.followee = u2

            relation.save()

            userList.append(u2)

        for u in userList:
            self.getNetwork(u.idstr, depth - 1)

    def getIDs(self):

        return network_target_ids

    def run(self):
        import pdb;pdb.set_trace()

        if "f" in self.option:
            ids = self.getIDs()
        else:
            if "ids" in self.option:
                ids = self.option["ids"]
                import pdb;pdb.set_trace()
            else:
                print "no ids specified!"
                return

        for id in ids:
            self.getNetwork(id, self.maxDepth)

        print "done"




class FetchStatusTask(BaseTask):

    def __init__(self, **option):
        """
        @param:
          option
            uid
            uids
        """

        BaseTask.__init__(self)

        self.option = option

    def getStatus(self, uid):

        COUNT = 100

        try:
            fetcher = StatusFetcher(uid=uid, count=1, page=1)
            url, resp, text = fetcher.fetch()

            rec = Record(url=url, date=datetime.datetime.now(), result_code=resp['status'], info='')
            rec.save()

        except:
            raise

        jsonObj = json.loads(text)

        if is_error(jsonObj):

            code, desc = check_error(jsonObj)

            print code,desc

            return

        total_number = jsonObj['total_number']

        page = 1

        while total_number > COUNT * page:

            try:
                fetcher = StatusFetcher(uid=uid, count=COUNT, page=page)

                url, resp, text = fetcher.fetch()
                rec = Record(url=url, date=datetime.datetime.now(), result_code=resp['status'], info='')
                rec.save()

            except:
                raise

            jsonObj = json.loads(text)

            if is_error(jsonObj):

                code, desc = check_error(jsonObj)

                print code, desc

                continue

            statuses = jsonObj['statuses']

            print len(statuses)

            stop = False

            # import pdb;pdb.set_trace()

            for status in statuses:

                # import pdb;pdb.set_trace()

                s = Status()

                try:
                    s = s.save_obj(status)
                except:
                    continue

                # tm = timezone.make_aware(s.created_at, timezone.get_default_timezone())
                tm = s.created_at

                # import pdb;pdb.set_trace()

                if not timezone.is_aware(tm):
                    tm = timezone.make_aware(tm, timezone.get_default_timezone())

                if "startDate" in self.option and self.option["startDate"] > tm:
                    print "stop condition meets."
                    print self.option["startDate"] , tm
                    stop = True

                if "endDate" in self.option and self.option["endDate"] < tm:
                    print "stop condition meets."
                    stop = True

                if stop:
                    return

            page += 1

            time.sleep(5)

    def run(self):

        if "uid" in self.option:
            self.getStatus(self.option["uid"])

        elif "uids" in self.option:

            for uid in self.option["uids"]:

                # import pdb;pdb.set_trace()

                self.getStatus(uid)

        print 'done'


########################################################################################################################


def get_init_page_view(request):

    return render_to_response('sinaapi/init.html')


def request_log_page_view(request):

    return HttpResponse('templates/sinaapi/request-log.html')


def get_request_log_view(request):

    new = request.GET['new'] if 'new' in request.GET else 0
    cnt = request.GET['cnt'] if 'cnt' in request.GET else 0


    if new:
        records = Record.objects.all().order_by('-id')[cnt]
    else:
        records = Record.objects.all()[cnt]

    return TemplateResponse(request, 'templates/sinaapi/request-log.html', {'records': records})


def get_conditional_status_request_page_view(request):
    """
    """

    form = ConditionalStatusRequestForm()

    d = dict()
    d.update({"form" : form})

    return render_to_response('sinaapi/request.html',d)

@csrf_exempt
def conditional_status_request_view(request):

    # import pdb;pdb.set_trace()

    form = ConditionalStatusRequestForm(request.POST)

    data = dict(form.data)

    if form.is_valid():

        users = form.cleaned_data["user"]
        uids = [u.idstr for u in users]

        startDate = form.cleaned_data["startDate"]
        endDate = form.cleaned_data["endDate"]

        task = FetchStatusTask(uids=uids, startDate=startDate)
        task.start()

        return HttpResponse("OK")


def get_single_user_view(request):

    uid = request.GET['uid']

    task = FetchSingleUserTask(uid)
    task.start()

    return HttpResponse(content=json.dumps({'status':'ok','msg': 'thread started'}),  mimetype='application/json')


def get_active_fans_view(request):

    uid = request.GET['uid']

    task = FetchUserActiveFansTask(uid)
    task.start()

    return HttpResponse(content=json.dumps({'status':'ok','msg': 'thread started'}),  mimetype='application/json')


def get_network_view(request):


    import pdb;pdb.set_trace()

    if u"f" in request.GET:
        task = FetchNetworkTask(f=1)
    else:
        idsStr = request.GET["ids"]
        ids = idsStr.split(",")

        task = FetchNetworkTask(ids=ids)
    task.start()

    return HttpResponse(content=json.dumps({'status':'ok','msg': 'thread started'}),  mimetype='application/json')


def get_all_status_view(request):

    uid = request.GET['uid']
    print uid

    task = FetchStatusTask(uid=uid)
    task.start()
    return HttpResponse(content=json.dumps({'status':'ok','msg': 'thread started'}),  mimetype='application/json')
