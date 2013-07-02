from django.db import models

# Create your models here.


# class EntityType(models.Model):
#
#     name = models.CharField(max_length=15)
#
#     def __unicode__(self):
#         return self.name
#
#
#     def save_type(self, *args, **kwargs):
#
#         if EntityType.objects.filter(name=self.name).exists():
#             self = EntityType.objects.get(name=self.name)
#         else:
#             super(EntityType, self).save()
#         return self