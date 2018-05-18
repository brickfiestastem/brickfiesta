from django.db import models
from event.utils import upload_path_event, upload_path_activity, upload_path_space
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


class Location(BaseModel):
    name = models.CharField(
        verbose_name='Name of Location', unique=True, max_length=128)
    street = models.CharField(verbose_name='Street', max_length=128)
    locality = models.CharField(verbose_name='City', max_length=64)
    region = models.CharField(verbose_name='State', max_length=64)
    postal_code = models.CharField(verbose_name='Postal Code', max_length=16)
    country = models.CharField(verbose_name='Country', max_length=3)
    phone_number = models.CharField(
        verbose_name='Phone Number', max_length=16, default='0000000000')
    url = models.URLField(verbose_name='URL', blank=True)
    latitude = models.FloatField(verbose_name='Latitude')
    longitude = models.FloatField(verbose_name='Longitude')

    def __str__(self):
        return self.name


class Space(BaseModel):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Venue Space Name', max_length=64)
    description = models.TextField(verbose_name='Description')
    map = models.ImageField(verbose_name='Map', null=True, blank=True,
                            upload_to=upload_path_event)
    max_seating = models.IntegerField(verbose_name='Max Seating')
    latitude = models.FloatField(
        verbose_name='Latitude', blank=True, null=True)
    longitude = models.FloatField(
        verbose_name='Longitude', blank=True, null=True)

    def __str__(self):
        return self.location.name + " - " + self.name


class Activity(BaseModel):
    title = models.CharField(verbose_name='Title', unique=True, max_length=64)
    description = models.TextField(verbose_name='Description')
    rules = models.TextField(verbose_name='Rules')
    materials_list = models.TextField(verbose_name='Materials List')
    picture = models.ImageField(
        upload_to=upload_path_activity, null=True, blank=True)
    signup_required = models.BooleanField(verbose_name='Sign Up Required')
    min_people = models.IntegerField(verbose_name='Minimum People')
    max_people = models.IntegerField(verbose_name='Maximum People')

    class Meta:
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.title


class ActivityVolunteers(BaseModel):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.SmallIntegerField(verbose_name='Order')


class Event(BaseModel):
    title = models.CharField(verbose_name='Title', unique=True, max_length=64)
    description = models.TextField(verbose_name='Description')
    hashtag = models.CharField(
        verbose_name='Hashtag', unique=True, max_length=16)
    theme = models.CharField(verbose_name='Theme', max_length=128)
    hotel_information = models.TextField(
        verbose_name='Hotel Information', null=True)
    hotel_code_url = models.URLField(
        verbose_name='Hotel Reservation Code', blank=True, default='')
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to=upload_path_event, null=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    @property
    def is_current(self):
        today = datetime.date.today()
        return self.start_date <= today and self.end_date >= today

    @property
    def is_past(self):
        today = datetime.date.today()
        return self.end_date < today

    @property
    def is_upcoming(self):
        today = datetime.date.today()
        return self.start_date > today


class Schedule(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return str(self.activity) + " in " + str(self.space) + " on " + str(self.date) + " @ " + str(self.start_time)

    class Meta:
        ordering = ("date", "event__title", "space__name", "start_time")
        unique_together = ("event", "space", "start_time", "date")
    # TODO: Event, Space, Date, and Time can't conflict.
