from django.db import models
from django.contrib.auth.models import User

import datetime
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class Business(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(
        verbose_name='Name of Business', unique=True, max_length=128)
    description = models.TextField(verbose_name='Description')
    street = models.CharField(verbose_name='Street Address', max_length=64)
    locality = models.CharField(verbose_name='Locality', max_length=64)
    region = models.CharField(verbose_name='Region', max_length=64)
    postal_code = models.CharField(verbose_name='Postal Code', max_length=16)
    country = models.CharField(verbose_name='Country', max_length=3)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=32)
    url = models.CharField(verbose_name='Website URL', max_length=255)
    logo = models.ImageField()


class BusinessNote(BaseModel):
    business = models.ForeignKey(Business)
    user = models.ForeignKey(User)
    note = models.TextField(verbose_name='Note')
