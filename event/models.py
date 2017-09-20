from django.db import models
import uuid

class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True

class Category(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='Name', unique=True, max_length=64)
    description = models.TextField(verbose_name='Description')
    age_limit_min = models.IntegerField(verbose_name='Minimum Age Limit')
    age_limit_max = models.IntegerField(verbose_name='Maximum Age Limit')

    def __str__(self):
        return self.name

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
    max_seating = models.IntegerField(verbose_name='Max Seating')
    location = models.ForeignKey(Location)
    latitude = models.FloatField(verbose_name='Latitude', blank=True)
    longitude = models.FloatField(verbose_name='Longitude', blank=True)

    def __str__(self):
        return self.name

class Event(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='Title', unique=True, max_length=64)
    description = models.TextField(verbose_name='Description')
    hashtag = models.CharField(verbose_name='Hashtag', unique=True, max_length=16)
    theme = models.CharField(verbose_name='Theme', max_length=128)
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    location = models.ForeignKey(Location)

    def __str__(self):
        return self.title

class InventoryItem(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    make = models.CharField(verbose_name='Make', max_length=64)
    model = models.CharField(verbose_name='Model', max_length=64)
    description = models.TextField(verbose_name='Description')
    serial_number = models.CharField(verbose_name='Serial Number', max_length=64)
    purchase_price = models.FloatField(verbose_name='Purchase Price')
    purchase_date = models.DateField(verbose_name='Date of Purchase')
    status = models.TextField(verbose_name='Status', max_length=64)
    condition = models.TextField(verbose_name='Condition', max_length=64)
    event = models.ForeignKey(Event)
    # user = models.ForeignKey(User)