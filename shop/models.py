from django.db import models
from django.contrib.auth.models import User
from event.models import Event
from referral.models import Referral
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True

class Product(BaseModel):


class Order(BaseModel):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    guest = models.CharField(max_length=255)
    referral = models.ForeignKey(Referral)