import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count

from afol.models import Fan
from event.models import Event, Space
from .utils import upload_path_mocs


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
    age_limit_min = models.IntegerField(
        verbose_name='Minimum Age Limit', default=0)
    age_limit_max = models.IntegerField(
        verbose_name='Maximum Age Limit', default=128)
    logo = models.ImageField(upload_to=upload_path_mocs, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['title', ]


class EventCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.title + " - " + self.category.title

    class Meta:
        verbose_name_plural = 'EventCategories'
        unique_together = ('category', 'event')
        ordering = ['-event', 'category']


class Moc(BaseModel):
    SIDE_FRONT = 1200
    SIDE_FRONT_RIGHT = 1330
    SIDE_RIGHT = 1500
    SIDE_BACK_RIGHT = 1630
    SIDE_BACK = 1800
    SIDE_BACK_LEFT = 1930
    SIDE_LEFT = 2100
    SIDE_FRONT_LEFT = 2300
    SIDES = (
        (SIDE_FRONT, 'Front'),
        (SIDE_FRONT_RIGHT, 'Front & Right'),
        (SIDE_RIGHT, 'Right'),
        (SIDE_BACK_RIGHT, 'Back & Right'),
        (SIDE_BACK, 'Back'),
        (SIDE_BACK_LEFT, 'Back & Left'),
        (SIDE_LEFT, 'Left'),
        (SIDE_FRONT_LEFT, 'Front & Left'),
    )
    creator = models.ForeignKey(
        Fan, on_delete=models.CASCADE, default=uuid.uuid4)
    title = models.CharField(verbose_name='Title', unique=True, max_length=64)
    description = models.TextField(verbose_name='Description',
                                   help_text='<ul><li>We limit this to 300 words on the table tent.</li></ul>')
    display_requirements = models.TextField(verbose_name='Display requirements',
                                            help_text='<ul><li>Does this MOC have special display requirements like power or something more than just table space? Enter it here.</li></ul>',
                                            blank=True, null=True)
    height = models.IntegerField(verbose_name='Height', default=10,
                                 help_text="<ul><li>Enter in inches rounded up to the nearest inch.</li></ul>")
    length = models.IntegerField(verbose_name='Length', default=10,
                                 help_text="<ul><li>Enter in inches rounded up to the nearest inch.</li>"
                                           "<li>This value is important as the software will not calculate the correct table space if this value is inaccurate.</li></ul>")
    width = models.IntegerField(verbose_name='Width', default=10,
                                help_text="<ul><li>Enter in inches rounded up to the nearest inch.</li>"
                                          "<li>This value is important as the software will not calculate the correct table space if this value is inaccurate.</li></ul>")
    viewable_sides = models.IntegerField(
        verbose_name='Viewable Sides', choices=SIDES, default=SIDE_FRONT)
    url_photo = models.URLField(
        verbose_name='URL Photo', blank=True, null=True)
    url_flickr = models.URLField(
        verbose_name='URL Flicker', blank=True, null=True)
    year_built = models.DateField(verbose_name='Year Build')
    year_retired = models.DateField(
        verbose_name='Year Retired', blank=True, null=True)
    is_public = models.BooleanField(
        verbose_name='Is Public',
        help_text='<ul><li>Visible on Brick Fiesta Website</li></ul>',
        default=False)

    class Meta:
        verbose_name_plural = 'MOCs'

    def __str__(self):
        return self.title


class MocNote(BaseModel):
    moc = models.ForeignKey(Moc, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField(verbose_name='Note')

    def __str__(self):
        return "{} note on {}".format(self.user, self.moc)


class MocCategories(BaseModel):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    moc = models.ForeignKey(Moc, on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {}".format(self.category, self.moc.title)


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
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE,
                            help_text="<ul><li>Please note that if the form doesn't submit then this fan"
                            " has already voted in this category.</li></ul>")
    moc = models.ForeignKey(Moc, on_delete=models.CASCADE)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)

    class Meta:
        unique_together = ('fan', 'category')

    objects = VoteManager()

    def save(self, *args, **kwargs):
        if self.value > 1:
            self.value = 1
        super(Vote, self).save(*args, **kwargs)


class PublicVote(BaseModel):
    session = models.UUIDField(verbose_name='Session ID')
    moc = models.ForeignKey(Moc, on_delete=models.CASCADE)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)


class Layout(BaseModel):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title', max_length=64)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    length = models.IntegerField()
    width = models.IntegerField()

    class Meta:
        unique_together = ('category', 'title')


class LayoutMoc(BaseModel):
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE)
    moc = models.ForeignKey(Moc, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()

    class Meta:
        unique_together = ('layout', 'moc')
