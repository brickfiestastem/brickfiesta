from django.db import models
from django.db.models import Count
from event.models import Event, Space
from django.conf import settings
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(verbose_name='Title', unique=True, max_length=64)
    description = models.TextField(verbose_name='Description')
    age_limit_min = models.IntegerField(verbose_name='Minimum Age Limit')
    age_limit_max = models.IntegerField(verbose_name='Maximum Age Limit')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'categories'


class EventCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=None)
    event = models.ForeignKey(Event, on_delete=None)

    class Meta:
        verbose_name_plural = 'EventCategories'
        unique_together = ('category', 'event')


class Moc(BaseModel):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None)
    category = models.ForeignKey(EventCategory, on_delete=None)
    moc = models.ForeignKey(Moc, on_delete=None)

    # TODO: Find a way to make the event and moc unique while still using eventcategory
    class Meta:
        unique_together = ('category', 'moc')


class VoteManager(models.Manager):
    def get_counts_by_event_category_uuid(self, event_category_uuid):
        # How to use: Vote.objects.get_counts("4def8511-873c-4cae-b1a3-f735f8a9e286")
        if isinstance(event_category_uuid, str):
            event_category_uuid = uuid.UUID(event_category_uuid)
        fieldname = "moc"
        category_votes = self.filter(category__category__id=event_category_uuid)\
            .values(fieldname).order_by(fieldname)\
            .annotate(the_count=Count(fieldname))
        return category_votes


class Vote(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None)
    moc = models.ForeignKey(Moc, on_delete=None)
    category = models.ForeignKey(EventCategory, on_delete=None)
    value = models.IntegerField(default=1)

    class Meta:
        unique_together = ('user', 'category')

    objects = VoteManager()

    def save(self, *args, **kwargs):
        if self.value > 1:
            self.value = 1
        super(Vote, self).save(*args, **kwargs)


class Layout(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None)
    category = models.ForeignKey(EventCategory, on_delete=None)
    title = models.CharField(verbose_name='Title', max_length=64)
    space = models.ForeignKey(Space, on_delete=None)
    length = models.IntegerField()
    width = models.IntegerField()

    class Meta:
        unique_together = ('category', 'title')


class LayoutMoc(BaseModel):
    layout = models.ForeignKey(Layout, on_delete=None)
    moc = models.ForeignKey(Moc, on_delete=None)
    x = models.IntegerField()
    y = models.IntegerField()

    class Meta:
        unique_together = ('layout', 'moc')
