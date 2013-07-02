from django.db import models

# Create your models here.


class Auth20AccessTokens(models.Model):

    app = models.CharField(max_length=31)
    access_token = models.CharField(max_length=127)

    def __unicode__(self):
        return self.app

class Auth20Config(models.Model):

    request = models.CharField(max_length=63)
    url = models.CharField(max_length=127)

    def __unicode__(self):
        return self.request


class Record(models.Model):

    url = models.CharField(max_length=255, verbose_name=u'request URL')

    date = models.DateTimeField(verbose_name=u'request date')

    result_code = models.CharField(max_length=15, verbose_name=u'HTTP respond status')

    info = models.TextField(verbose_name=u'request information')

    def __unicode__(self):
        return self.url


#
# class RequestTask(models.Model):
#
#     request = models.CharField(max_length=1024)
#
#     processor = models.IntegerField()
#
#     finished = models.BooleanField(default=False)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
#     def __unicode__(self):
#         return self.request