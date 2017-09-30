from django.db import models
import datetime
import uuid

class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True

class Location(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='Name of Location', unique=True, max_length=128)
    street = models.CharField(verbose_name='Street', max_length=128)
    locality = models.CharField(verbose_name='City', max_length=64)
    region = models.CharField(verbose_name='State', max_length=64)
    postal_code = models.CharField(verbose_name='Postal Code', max_length=16)
    country = models.CharField(verbose_name='Country', max_length=3)
    latitude = models.FloatField(verbose_name='Latitude')
    longitude = models.FloatField(verbose_name='Longitude')

    def __str__(self):
        return self.name

class Space(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='Venue Space Name', max_length=64)
    description = models.TextField(verbose_name='Description')
    url_image = models.URLField(verbose_name='Image')
    max_seating = models.IntegerField(verbose_name='Max Seating')
    location = models.ForeignKey(Location)
    latitude = models.FloatField(verbose_name='Latitude', blank=True, null=True)
    longitude = models.FloatField(verbose_name='Longitude', blank=True, null=True)

    def __str__(self):
        return self.name

class Activity(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='Title', unique=True, max_length=64)
    description = models.TextField(verbose_name='Description')
    rules = models.TextField(verbose_name='Rules')
    materials_list = models.TextField(verbose_name='Materials List')
    signup_required = models.BooleanField(verbose_name='Sign Up Required')
    min_people = models.IntegerField(verbose_name='Minimum People')
    max_people = models.IntegerField(verbose_name='Maximum People')

class Event(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='Title', unique=True, max_length=64)
    description = models.TextField(verbose_name='Description')
    hashtag = models.CharField(verbose_name='Hashtag', unique=True, max_length=16)
    theme = models.CharField(verbose_name='Theme', max_length=128)
    hotel_information = models.TextField(verbose_name='Hotel Information', null=True)
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    location = models.ForeignKey(Location)

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
