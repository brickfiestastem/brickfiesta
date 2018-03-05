from django.db import models
from django.contrib.auth.models import User
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


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    bricklink_username = models.CharField(max_length=64, blank=True)
    twitter_handle = models.CharField(max_length=64, blank=True)
    flickr_handle = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ('user__first_name', 'user__last_name')

    def __str__(self):
        return "{} {} - {}".format(self.user.first_name, self.user.last_name, self.user.email)


class Attendee(BaseModel):
    ROLES = (
        ('co-chair', 'Co-Chair'),
        ('volunteer', 'Volunteer'),
        ('sponsor', 'Sponsor'),
        ('vendor', 'Vendor'),
        ('attendee', 'Attendee'),
    )
    event = models.ForeignKey(Event, on_delete=None)
    user = models.ForeignKey(User, on_delete=None)
    role = models.CharField(max_length=16, choices=ROLES)


class Badge(BaseModel):
    user = models.ForeignKey(User, on_delete=None)
    event = models.ForeignKey(Event, on_delete=None)
    badge_name = models.CharField(max_length=32, blank=False)
    rlug_name = models.CharField(max_length=32, blank=False)
    locality = models.CharField(max_length=32, blank=False)
    region = models.CharField(max_length=32, blank=False)
    date_ordered = models.DateField(verbose_name='Date Ordered', null=True)


class ShirtSizesAvailable(BaseModel):
    event = models.ForeignKey(Event, on_delete=None)
    shirt_size = models.CharField(max_length=8)


class Shirt(BaseModel):
    user = models.ForeignKey(User, on_delete=None)
    event = models.ForeignKey(Event, on_delete=None)
    shirt_size = models.CharField(max_length=8)
