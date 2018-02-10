from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
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


class User(BaseModel, AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    bricklink_username = models.CharField(max_length=64, blank=True)
    twitter_handle = models.CharField(max_length=64, blank=True)
    flickr_handle = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ('first_name', 'last_name')

    def __str__(self):
        return "{} {} - {}".format(self.first_name, self.last_name, self.email)


class Attendee(BaseModel):
    ROLES = (
        ('co-chair', 'Co-Chair'),
        ('volunteer', 'Volunteer'),
        ('sponsor', 'Sponsor'),
        ('vendor', 'Vendor'),
        ('attendee', 'Attendee'),
    )
    event = models.ForeignKey(Event, on_delete=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None)
    role = models.CharField(max_length=16, choices=ROLES)


class Badge(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None)
    event = models.ForeignKey(Event, on_delete=None)
    badge_name = models.CharField(max_length=32, blank=False)
    rlug_name = models.CharField(max_length=32, blank=False)
    locality = models.CharField(max_length=32, blank=False)
    region = models.CharField(max_length=32, blank=False)
    date_ordered = models.DateField(verbose_name='Date Ordered', null=True)


class Shirt(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None)
    event = models.ForeignKey(Event, on_delete=None)
    shirt_size = models.CharField(max_length=8)
