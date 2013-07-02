from django.http import HttpResponse
from django.db.models import Q


from django.template.loader import get_template
from django.template import Context

import threading
import json

from network.models import (
    Status,
    SNUserRelation,
    SNUser,
    )

from ner.models import (
    EntityType,
    Entity,
    Tag,
    Candidate,
    RecognizeRecord,
    RecognitionUserRecord,
    RecordStatusRelation,
    RecordEntityRelation
    )

from ner.recognition.test import (
    test,
    )
from ner.recognition.data import (
    load_config,
    process_at_person,
    process_url,
    xml2bio,
    )
from ner.recognition.feature import (
    create_tags,
    stringify_feature_vecter_with_cate,
    )

from shared.util import (
    set_value,
    )

# Create your views here.

########################################################################################################################

class StartTestTask(threading.Thread):

    def __init__(self, **option):

        threading.Thread.__init__(self)

        self.uidrec = None
        self.config = load_config()
        self.option = option

        self.sns = self.option['sns'] if 'sns' in self.option else False

    def printSNSStatus(self):

        status = "current target: %s."%self.rtarget
        status += "%d of %d follows effects."%(self.reffectUserCount, self.ruserCount)
        status += "%d of %d status effects."%(self.reffectStatusCount, self.rstatusCount)
        status += "%d of %d entity effects."%(self.reffectEntityCount, self.rentityCount)
        return status

    def getRecommendCate(self, target):
        """
        records following information:
            effective entity: id of entity


        """

        recogRecord = RecognizeRecord()

        self.rtarget = target

        # get current user by id
        u = SNUser.objects.get(idstr=self.uidrec)

        # get the relationship
        rels = SNUserRelation.objects.filter(followee=u)

        # to get the followers
        users = [r.follower for r in rels]

        self.ruserCount = len(users)

        # to record each user's recommendation
        userEntityRecord = dict()

        self.rstatusCount = 0
        self.reffectStatusCount = 0
        self.rentityCount = 0
        self.reffectEntityCount = 0

        # for each user who followed current user
        for user in users:

            userRecordInserted = False

            statuses = Status.objects.filter(user=user)

            entitySet = {}

            dorminator = .0

            for s in statuses:

                statusCounted = False

                statusRecordInserted = False

                entities = Entity.objects.filter(status=s).exclude(tag__type__name=u"N")



                for e in entities:

                    entityRecordInserted = False

                    t = e.tag.type.name
                    p = e.tag.p

                    # TODO: t is not 'N'
                    if e.content == target:

                        # import pdb
                        # pdb.set_trace()

                        if not userRecordInserted:
                            # TODO: insert user record
                            userRecord = RecognitionUserRecord(record=recogRecord, user=user)
                            userRecordInserted = True


                        if not statusRecordInserted:
                            # TODO: insert status record
                            statusRecord = RecordStatusRelation(userRecord=userRecord, status=s)
                            statusRecordInserted = True

                        if not entityRecordInserted:
                            # TODO: insert entity record
                            entityRecord = RecordEntityRelation(statusRecord=statusRecord, entity=e)
                            entityRecordInserted = True



                        if t not in entitySet:
                            entitySet[t] = .0

                        entitySet[t] += p
                        dorminator += p

                        if not statusCounted:

                            self.reffectStatusCount += 1
                            statusCounted = True

                        self.reffectEntityCount += 1
                    self.rentityCount += 1

                self.rstatusCount += 1

            if len(entitySet) == 0 or dorminator == 0:
                print dorminator
                continue

            import pdb;pdb.set_trace()

            # normalization
            for t in entitySet:
                entitySet[t] /= dorminator

            # to get the entity type of one user
            it = iter(entitySet)
            maxLikelyType = it.next()
            maxLikelihood = entitySet[maxLikelyType]

            for t in it:
                curType = t
                curLikelihood = entitySet[curType]

                # TODO: only add the entity whose type is not 'N'

                if curLikelihood > maxLikelihood:
                    maxLikelyType = curType
                    maxLikelihood = curLikelihood



            if maxLikelyType not in userEntityRecord:
                userEntityRecord[user.id] = .0

            userEntityRecord[user.id] = (maxLikelyType, maxLikelihood,)




        # to record how many people participates in
        self.reffectUserCount = len(userEntityRecord)

        # no user or no entity
        if len(userEntityRecord) == 0:
            print 0
            return 'N', 0.0, recogRecord


        #TODO: for each user's recommandation, times an user's authority.


        import pdb;pdb.set_trace()

        it = iter(userEntityRecord)

        maxLikelyUser = it.next()
        maxLikelyType, maxLikelihood = userEntityRecord[maxLikelyUser]

        for user in it:
            curU = user
            curType, curLikelihood = userEntityRecord[curU]

            if curLikelihood > maxLikelihood:
                maxLikelyType = curType
                maxLikelihood = curLikelihood
                maxLikelyUser = curU

        # TODO: set a threshold
        return maxLikelyType, maxLikelihood, recogRecord

    def test(self, inputParam, tags, records, status):

        assert len(records) == len(tags), "lengthes of tags and records are not equal"

        results = test(inputParam, tags)

        # for one piece of weibo
        pos = 0
        for i in xrange(len(results)):

            token = results[i]



            # current word
            word = token[0]

            # get the most likely cate
            most = token[1]

            # the all possible categories of current token
            cates = token[2]

            # unzip the element
            cate, p, alpha, beta = most

            entity = Entity()
            entity.save_entity(status, cate=cate, p=p, alpha=alpha, beta=beta, content=word, text='', pos=pos, sns=self.sns)

            rec = records[i]

            rec.entity = rec

            import pdb;pdb.set_trace()

            rec.save()

            print rec.id

            # to get the first token, which is the most likely category
            # it = iter(cates)
            # for other in it:
            #
            #     cand = Candidate()
            #
            #     cate, p, alpha, beta = other
            #
            #     cand.save_candidate(entity, cate=cate, p=p, alpha=alpha, beta=beta)

            pos += 1

    def test_without_sns(self, inputParam, statuses):

        for status in statuses:

            # preprocess
            text = status.text
            text = process_at_person(text)
            text = process_url(text)

            tags = create_tags(text)

            self.test(inputParam, tags, status)

    def test_with_sns(self, inputParam, statuses):

        import pdb;pdb.set_trace()

        for status in statuses:

            # preprocess
            text = status.text
            text = process_at_person(text)
            text = process_url(text)

            tags = []

            tokens = xml2bio(text)

            recs = []

            for t in tokens:

                w = t[0]

                # to record current user id
                self.uidrec = status.user.idstr

                c, p, rec = self.getRecommendCate(w)

                recs.append(rec)

                print self.printSNSStatus()
                print w, c
                tags.append(w + ' ' + c[0])

            import pdb;pdb.set_trace()
            self.test(inputParam, tags, recs, status)

    def recognize(self, statuses):
        """
        """

        # to get the pieces of specific user
        if self.sns:
            inputParam = '-m %s -v 3 -n2'%(self.config['model_sns'])

            self.test_with_sns(inputParam, statuses)
        else:
            inputParam = '-m %s -v 3 -n2'%(self.config['model'])

            self.test_without_sns(inputParam, statuses)


    def run(self):

        import pdb;pdb.set_trace()

        cond = Q()

        if 'gte' in self.option:
            cond &= Q(id__gte=self.option['gte'])

        if 'lte' in self.option:
            cond &= Q(id__lte=self.option['lte'])

        if 'rand' in self.option and self.option['rand']:

            if 'ids' in self.option:
                ids = self.option['ids'].split(',')
                cond &= Q(idstr__in=ids)

        else:

            if 'uid' in self.option:
                cond &= Q(user__idstr=self.option['uid'])

        statuses = Status.objects.filter(cond)

        self.recognize(statuses)

        print 'done'




########################################################################################################################


def recognize_entity_view(request):

    option = dict()

    sns = int(set_value('sns', request.GET, 0))
    rand = int(set_value('sns', request.GET, 0))
    sns = False if sns == 0 else True
    rand = False if rand == 0 else True

    option['sns'] = sns
    option['rand'] = rand

    import pdb;pdb.set_trace()




    if 'uid' in request.GET:

        if 'gte' in request.GET:
            gte = request.GET['gte']
            option['gte'] = gte


        uid = request.GET['uid']

        option['uid'] = uid



    # batch recognize the status selected by relative word
    elif 'ids' in request.GET:

        ids = request.GET["ids"]
        option["ids"] = ids


    task = StartTestTask(**option)

    task.start()

    return HttpResponse(content=json.dumps({'status':'ok','msg': 'thread started'}),  mimetype='application/json')










def get_entity_view(request):


    # import pdb;pdb.set_trace()

    if 'wid' in request.GET:

        wid = request.GET['wid']

        entityQuerySet = Entity.objects.filter(status__wid=wid)

        template = get_template('snippets/entity-of-status-snippet.html')

        context = Context({'entities':entityQuerySet})

        rendered = template.render(context)

        return HttpResponse(rendered)

    else:
        return HttpResponse('')






def test_view1(request):
    return HttpResponse(content=json.dumps({'status':'ok','msg': 'thread started'}),  mimetype='application/json')

