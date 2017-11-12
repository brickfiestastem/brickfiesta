from django.db import models
from django.contrib.auth.models import User
from event.models import Event
from referral.models import Referral
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class ProductType(BaseModel):
    title = models.CharField(max_length=64)
    description = models.TextField()


class Product(BaseModel):
    event = models.ForeignKey(Event)
    product_type = models.ForeignKey(ProductType)
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField()


class Order(BaseModel):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    guest = models.CharField(max_length=255)
    referral = models.ForeignKey(Referral)
