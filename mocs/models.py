from django.db import models
from event.models import Event, Space
from django.contrib.auth.models import User
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True

class Category(BaseModel):
    title = models.CharField(verbose_name='Title', unique=True, max_length=64)
    description = models.TextField(verbose_name='Description')
    age_limit_min = models.IntegerField(verbose_name='Minimum Age Limit')
    age_limit_max = models.IntegerField(verbose_name='Maximum Age Limit')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class EventCategory(BaseModel):
    category = models.ForeignKey(Category)
    event = models.ForeignKey(Event)

    class Meta:
        verbose_name_plural = 'EventCategories'
        unique_together = ('category', 'event')

class Moc(BaseModel):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    title = models.CharField(verbose_name='Title', unique=True, max_length=64)
    description = models.TextField(verbose_name='Description')
    height = models.IntegerField(verbose_name='Height')
    length = models.IntegerField(verbose_name='Length')
    width = models.IntegerField(verbose_name='Width')
    viewable_sides = models.IntegerField(verbose_name='Viewable Sides')
    url_photo = models.URLField(verbose_name='URL Photo')
    url_flickr = models.URLField(verbose_name='URL Flicker')
    year_build = models.DateField(verbose_name='Year Build')
    year_retired = models.DateField(verbose_name='Year Retired')

    def __str__(self):
        return self.title

class EventMoc(BaseModel):
    user = models.ForeignKey(User)
    category = models.ForeignKey(EventCategory)
    moc = models.ForeignKey(Moc)

    # TODO: Find a way to make the event and moc unique while still using eventcategory

class Layout(BaseModel):
    user = models.ForeignKey(User)
    category = models.ForeignKey(EventCategory)
    title = models.CharField(verbose_name='Title', max_length=64)
    space = models.ForeignKey(Space)
    length = models.IntegerField()
    width = models.IntegerField()

    class Meta:
        unique_together = ('category', 'title')

class LayoutMoc(BaseModel):
    layout = models.ForeignKey(Layout)
    moc = models.ForeignKey(Moc)
    x = models.IntegerField()
    y = models.IntegerField()

    class Meta:
        unique_together = ('layout', 'moc')