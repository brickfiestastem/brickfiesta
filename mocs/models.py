from django.db import models
from event.models import Event
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


class EventCategory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category)
    event = models.ForeignKey(Event)


class Moc(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='Title', unique=True, max_length=64)
    description = models.TextField(verbose_name='Description')
    height = models.IntegerField(verbose_name='Height')
    length = models.IntegerField(verbose_name='Length')
    width = models.IntegerField(verbose_name='Width')
    viewable_sides = models.IntegerField(verbose_name='Viewable Sides')
    url_photo = models.URLField(verbose_name='URL Photo')
    url_flicker = models.URLField(verbose_name='URL Flicker')
    year_build = models.DateField(verbose_name='Year Build')
    year_retired = models.DateField(verbose_name='Year Retired')

    def __str__(self):
        return self.title
