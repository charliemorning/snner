from django.db import models
from django.db import transaction

from network.models import Status,SNUser

from shared.util import set_value


class EntityType(models.Model):

    name = models.CharField(max_length=15)

    def __unicode__(self):
        return self.name

    def save_type(self, *args, **kwargs):

        if EntityType.objects.filter(name=self.name).exists():
            self = EntityType.objects.get(name=self.name)
        else:
            super(EntityType, self).save()
        return self


class Tag(models.Model):

    type = models.ForeignKey(EntityType)
    p = models.FloatField()
    alpha = models.FloatField()
    beta = models.FloatField()

    def save_tag(self, *args, **kwargs):

        cate = set_value('cate', kwargs, 'N')

        entityType = EntityType()
        entityType.name = cate
        entityType = entityType.save_type()

        self.type = entityType
        self.p = set_value('p', kwargs, self.p)
        self.alpha = set_value('alpha', kwargs, self.alpha)
        self.beta = set_value('beta', kwargs, self.beta)

        super(Tag, self).save()
        return self


class Entity(models.Model):

    tag = models.ForeignKey(Tag)

    status = models.ForeignKey(Status)

    # the text of status
    text = models.CharField(max_length=255)

    # the content of entity
    content = models.CharField(max_length=31)

    begin = models.IntegerField()

    end = models.IntegerField()

    sns = models.BooleanField(default=False)

    def save_entity(self, status, *args, **kwargs):

        tag = Tag()
        tag.p = set_value('p', kwargs, .0)
        tag.alpha = set_value('alpha', kwargs, .0)
        tag.beta = set_value('beta', kwargs, .0)

        tag = tag.save_tag(cate=kwargs['cate'])

        self.tag = tag
        self.status = status

        self.content = set_value('content', kwargs, '')
        self.text = set_value('text', kwargs, '')

        self.begin = set_value('pos', kwargs, 0)
        self.end = set_value('pos', kwargs, 0) + 1

        self.sns = set_value("sns", kwargs, False)

        super(Entity, self).save()

        return self

    def __unicode__(self):
        return self.content


class Candidate(models.Model):

    entity =  models.ForeignKey(Entity)

    tag = models.ForeignKey(Tag)

    def save_candidate(self, entity, *args, **kwargs):

        tag = Tag()

        tag.p = set_value('p', kwargs, .0)
        tag.alpha = set_value('alpha', kwargs, .0)
        tag.beta = set_value('beta', kwargs, .0)

        tag = tag.save_tag(cate=kwargs['cate'])

        self.tag = tag

        self.entity = entity

        super(Candidate, self).save()

        return self


class RecognizeRecord(models.Model):

    entity = models.ForeignKey(Entity)

    def save_record(self):

        pass

    def __unicode__(self):
        pass


class RecognitionUserRecord(models.Model):

    record = models.ForeignKey(RecognizeRecord)
    user = models.ForeignKey(SNUser)

    def save_user_record(self):
        pass

    def __unicode__(self):
        pass


class RecordStatusRelation(models.Model):

    userRecord = models.ForeignKey(RecognitionUserRecord)
    status = models.ForeignKey(Status)

    def save_status_record(self):
        pass

    def __unicode__(self):
        pass


class RecordEntityRelation(models.Model):

    statusRecord = models.ForeignKey(RecordStatusRelation)
    entity = models.ForeignKey(Entity)

    def save_entity_record(self):
        pass

    def __unicode__(self):
        pass