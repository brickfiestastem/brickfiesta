from django.db import models
from django.contrib.auth.models import User
from event.models import Event
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


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

#    class Meta:
#        unique_together = ("event", "fan", "role")

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

#    class Meta:
#        unique_together = ("event", "fan")

    def __str__(self):
        return "{} - Badge {}".format(self.fan, self.event.title)


class Shirt(BaseModel):
    SHIRT_SIZES_ADULTM = 'AM'
    SHIRT_SIZES = (
        ('AS', 'Adult S'),
        (SHIRT_SIZES_ADULTM, 'Adult M'),
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
    shirt_size = models.CharField(max_length=8, choices=SHIRT_SIZES, default=SHIRT_SIZES_ADULTM)

#    class Meta:
#        unique_together = ("event", "fan")

    def __str__(self):
        return "{} {} - {}, {}".format(self.fan.first_name, self.fan.last_name, self.get_shirt_size_display(), self.event.title)
