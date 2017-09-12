from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True

class Location(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='Name of Location', max_length=128)
    street = models.CharField(verbose_name='Street', max_length=128)
    locality = models.CharField(verbose_name='City', max_length=64)
    region = models.CharField(verbose_name='State', max_length=64)
    postal_code = models.CharField(verbose_name='Postal Code', max_length=16)
    latitude = models.FloatField(verbose_name='Latitude')
    longitude = models.FloatField(verbose_name='Longitude')


