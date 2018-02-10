from django.db import models
# from django.conf import settings
from event.models import Event
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class Referral(BaseModel):
    event = models.ForeignKey(Event, on_delete=None)
    group_name = models.CharField(max_length=64)
    description = models.TextField()
    code = models.UUIDField(default=uuid.uuid4, editable=False)
