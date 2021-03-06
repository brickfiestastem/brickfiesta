import uuid

from barcode import generate
from barcode.writer import ImageWriter
from io import BytesIO
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from event.models import Event, Schedule
from .utils import upload_path_barcodes


def get_user_string(self):
    return self.first_name + " " + self.last_name + " (" + self.email + ")"


User.add_to_class("__str__", get_user_string)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class Fan(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=128)
    birth_date = models.DateField(null=True, blank=True)
    bar_code = models.ImageField(
        upload_to=upload_path_barcodes, null=True, blank=True)

    def generate_barcode(self):
        buffer = BytesIO()
        generate('CODE128', str(self.id), writer=ImageWriter(), output=buffer,
                 text=self.first_name + ' ' + self.last_name)
        filename = 'barcode-%s.png' % str(self.id)
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', buffer.__sizeof__(), None)
        self.bar_code.save(filename, filebuffer)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


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


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # TODO: Fix so the profile and fan names are synced
        Fan.objects.create(
            user=instance, first_name=instance.first_name, last_name=instance.last_name)
        Profile.objects.create(user=instance)
    instance.profile.save()


class Attendee(BaseModel):
    ROLE_COCHAIR = 'co-chair'
    ROLE_VOLUNTEER = 'volunteer'
    ROLE_SPONSOR = 'sponsor'
    ROLE_VENDOR = 'vendor'
    ROLE_ATTENDEE = 'attendee'
    ROLE_ALLACCESS = 'allaccess'
    ROLE_COMPANION = 'companion'

    ROLES = (
        (ROLE_COCHAIR, 'Co-Chair'),
        (ROLE_VOLUNTEER, 'Volunteer'),
        (ROLE_SPONSOR, 'Sponsor'),
        (ROLE_VENDOR, 'Vendor'),
        (ROLE_ATTENDEE, 'Attendee'),
        (ROLE_ALLACCESS, 'All Access'),
        (ROLE_COMPANION, 'Companion'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    role = models.CharField(max_length=16, choices=ROLES)

    class Meta:
        unique_together = ("event", "fan", "role")

    def __str__(self):
        return "{} {} - {}, {}".format(self.fan.first_name, self.fan.last_name, self.get_role_display(), self.event.title)


class Badge(BaseModel):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    badge_name = models.CharField(max_length=32, blank=False)
    rlug_name = models.CharField(max_length=32, blank=True)
    locality = models.CharField(max_length=32, blank=True)
    region = models.CharField(max_length=32, blank=True)
    date_ordered = models.DateField(
        verbose_name='Date Ordered', null=True, blank=True)

    class Meta:
        unique_together = ("event", "fan")

    def __str__(self):
        return "{} - Badge {}".format(self.fan, self.event.title)


class Shirt(BaseModel):
    SHIRT_SIZE_UNDEFINED = 'NS'
    SHIRT_SIZES = (
        (SHIRT_SIZE_UNDEFINED, 'Not Specified'),
        ('AS', 'Adult S'),
        ('AM', 'Adult M'),
        ('AL', 'Adult L'),
        ('AXL', 'Adult XL'),
        ('A2XL', 'Adult 2XL'),
        ('A3XL', 'Adult 3XL'),
        ('A4XL', 'Adult 4XL'),
        ('A5XL', 'Adult 5XL'),
        ('YXS', 'Youth XS'),
        ('YS', 'Youth S'),
        ('YM', 'Youth M'),
        ('YL', 'Youth L'),
    )
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    shirt_size = models.CharField(
        max_length=8, choices=SHIRT_SIZES, default=SHIRT_SIZE_UNDEFINED)
    date_ordered = models.DateField(
        verbose_name='Date Ordered', null=True, blank=True)

    class Meta:
        unique_together = ("event", "fan")

    def __str__(self):
        return "{} {} - {}, {}".format(self.fan.first_name, self.fan.last_name, self.get_shirt_size_display(), self.event.title)


class ScheduleVolunteer(BaseModel):

    def volunteernumber():
        return 1

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(
        verbose_name='Volunteer Order', default=volunteernumber)

    class Meta:
        unique_together = ("schedule", "fan")

    def __str__(self):
        return "{} is the {} volunteer for {}".format(self.fan, self.order, self.schedule)


class ScheduleAttendee(BaseModel):

    def attendeenumber():
        return 1

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(
        verbose_name='Sign Up Order', default=attendeenumber)
    has_attended = models.BooleanField(
        verbose_name='Attended Event', default=False)

    class Meta:
        unique_together = ("schedule", "fan")

    def __str__(self):
        return "{} is the {} attendee for {}".format(self.fan, self.order, self.schedule)
