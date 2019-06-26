import uuid

from django.db import models

# from django.conf import settings
from event.models import Event


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class Referral(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=64)
    description = models.TextField()
    url = models.URLField(default='https://www.brickfiesta.com/')
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    count = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return "Refer {} to {}".format(self.code, self.url)
