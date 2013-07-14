from django.db import models
import json
import datetime

from shared.util import parse_datestr

# Create your models here.





class SNUser(models.Model):


    idstr = models.CharField(max_length=15)
    name = models.CharField(max_length=255,null=True)

    screen_name = models.CharField(max_length=255,null=True)

    domain = models.CharField(max_length=255,null=True)

    gender = models.CharField(max_length=3, null=True)
    location = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=5, null=True)
    province = models.CharField(max_length=5, null=True)
    lang = models.CharField(max_length=15, null=True)
    description = models.CharField(max_length=1023, null=True)

    verified = models.NullBooleanField(null=True)

    bi_followers_count = models.IntegerField(null=True)
    followers_count = models.IntegerField(null=True)
    friends_count = models.IntegerField(null=True)
    statuses_count = models.IntegerField(null=True)
    favourites_count = models.IntegerField(null=True)
    online_status = models.IntegerField(null=True)
    block_word = models.IntegerField(null=True)
    star = models.IntegerField(null=True)

    allow_all_comment = models.NullBooleanField(null=True)
    allow_all_act_msg = models.NullBooleanField(null=True)
    geo_enabled = models.NullBooleanField(null=True)

    profile_url = models.CharField(max_length=31, null=True)
    profile_image_url = models.CharField(max_length=255, null=True)
    avatar_large = models.URLField(null=True)


    created_at = models.DateTimeField(null=True)
    insert_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


    def save_obj(self, jsonObj, *args, **kwargs):

        self.idstr = jsonObj['idstr'] if 'idstr' in jsonObj else ''

        if SNUser.objects.filter(idstr=self.idstr).exists():
            print 'exists!'
            self = SNUser.objects.get(idstr=self.idstr)


        self.name = jsonObj['name'] if 'name' in jsonObj else ''
        self.screen_name = jsonObj['screen_name'] if 'screen_name' in jsonObj else ''
        self.domain = jsonObj['domain'] if 'domain' in jsonObj else ''
        self.gender = jsonObj['gender'] if 'gender' in jsonObj else ''
        self.location = jsonObj['location'] if 'location' in jsonObj else ''
        self.city = jsonObj['city'] if 'city' in jsonObj else ''
        self.province = jsonObj['province'] if 'province' in jsonObj else ''
        self.lang = jsonObj['lang'] if 'lang' in jsonObj else ''
        self.description = jsonObj['description'] if 'description' in jsonObj else ''
        self.verified = jsonObj['verified'] if 'verified' in jsonObj else False
        self.bi_followers_count = jsonObj['bi_followers_count'] if 'bi_followers_count' in jsonObj else 0
        self.followers_count = jsonObj['followers_count'] if 'followers_count' in jsonObj else 0
        self.friends_count = jsonObj['friends_count'] if 'friends_count' in jsonObj else 0
        self.statuses_count = jsonObj['statuses_count'] if 'statuses_count' in jsonObj else 0
        self.favourites_count = jsonObj['favourites_count'] if 'favourites_count' in jsonObj else 0
        self.online_status = jsonObj['online_status'] if 'online_status' in jsonObj else 0
        self.block_word = jsonObj['block_word'] if 'block_word' in jsonObj else 0
        self.star = jsonObj['star'] if 'star' in jsonObj else 0
        self.allow_all_comment = jsonObj['allow_all_comment'] if 'allow_all_comment' in jsonObj else True
        self.allow_all_act_msg = jsonObj['allow_all_act_msg'] if 'allow_all_act_msg' in jsonObj else True
        self.geo_enabled = jsonObj['geo_enabled'] if 'geo_enabled' in jsonObj else False
        self.profile_url = jsonObj['profile_url'] if 'profile_url' in jsonObj else ''
        self.profile_image_url = jsonObj['profile_image_url'] if 'profile_image_url' in jsonObj else ''
        self.avatar_large = jsonObj['avatar_large'] if 'avatar_large' in jsonObj else ''


        self.created_at = parse_datestr(jsonObj['created_at']) if 'created_at' in jsonObj else datetime.datetime.now()

        try:
            super(SNUser, self).save(*args, **kwargs)
        except:
            print "error"
            return


    def save_str(self, jsonStr, *args, **kwargs):

        jsonObj = json.loads(jsonStr)

        self.save_obj(jsonObj, *args, **kwargs)






    def __unicode__(self):
        return self.name




class SNUserRelation(models.Model):

    follower = models.ForeignKey(SNUser, on_delete=models.CASCADE, related_name='follower_id')
    followee = models.ForeignKey(SNUser, on_delete=models.CASCADE, related_name='followee_id')

    def __unicode__(self):
        return u'%s -> %s'%(self.follower.name, self.followee.name)


class Status(models.Model):

    user = models.ForeignKey(SNUser)

    wid = models.CharField(max_length=63)
    mid = models.CharField(max_length=63)
    idstr = models.CharField(max_length=255)

    text = models.CharField(max_length=1024)

    truncated = models.BooleanField()

    source = models.CharField(max_length=255)

    comments_count = models.IntegerField()
    reposts_count = models.IntegerField()
    attitudes_count = models.IntegerField()


    bmiddle_pic = models.CharField(max_length=255)
    original_pic = models.CharField(max_length=255)
    thumbnail_pic = models.CharField(max_length=255)

    geox = models.FloatField()
    geoy = models.FloatField()

    created_at = models.DateTimeField()
    insert_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.id


    def save_obj(self, jsonObj, *args, **kwargs):

        self.wid = jsonObj['id'] if 'id' in jsonObj else ''

        #import pdb; pdb.set_trace()

        if Status.objects.filter(wid=self.wid).exists():
            print 'status exists!'
            self = Status.objects.get(wid=self.wid)
            return self



        self.mid = jsonObj['mid'] if 'mid' in jsonObj else ''
        self.idstr = jsonObj['idstr'] if 'idstr' in jsonObj else ''
        self.text = jsonObj['text'] if 'text' in jsonObj else ''

        self.truncated = jsonObj['truncated'] if 'truncated' in jsonObj else False
        #self.source = jsonObj['source'] if 'source' in jsonObj else ''
        self.source = ''

        self.comments_count = jsonObj['comments_count'] if 'comments_count' in jsonObj else 0
        self.reposts_count = jsonObj['reposts_count'] if 'reposts_count' in jsonObj else 0
        self.attitudes_count = jsonObj['attitudes_count'] if 'attitudes_count' in jsonObj else 0

        self.bmiddle_pic = jsonObj['bmiddle_pic'] if 'bmiddle_pic' in jsonObj else ''
        self.original_pic = jsonObj['original_pic'] if 'original_pic' in jsonObj else ''
        self.thumbnail_pic = jsonObj['thumbnail_pic'] if 'thumbnail_pic' in jsonObj else ''


        if 'geo' in jsonObj and  jsonObj['geo']:
                self.geox = jsonObj['geo']['coordinates'][0]
                self.geoy = jsonObj['geo']['coordinates'][1]

        else:
            self.geox = .0
            self.geoy = .0



        self.created_at = parse_datestr(jsonObj['created_at']) if 'created_at' in jsonObj else datetime.datetime.now()


        if 'user' in jsonObj:
            uid = jsonObj['user']['id']

            self.user = SNUser.objects.get(idstr=uid)


        try:
            super(Status, self).save(*args, **kwargs)
        except:
            print "failto save status!"
            raise

        return self



    def save_str(self, jsonStr, *args, **kwargs):

        jsonObj = json.loads(jsonStr)

        return self.save_obj(jsonObj, *args, **kwargs)



