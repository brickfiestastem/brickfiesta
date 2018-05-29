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
        return "{} {} - {}".format(self.first_name, self.last_name, self.user.email)


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
        Fan.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name)
        Profile.objects.create(user=instance)
    instance.profile.save()


class Attendee(BaseModel):
    ROLES = (
        ('co-chair', 'Co-Chair'),
        ('volunteer', 'Volunteer'),
        ('sponsor', 'Sponsor'),
        ('vendor', 'Vendor'),
        ('attendee', 'Attendee'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    role = models.CharField(max_length=16, choices=ROLES)

    class Meta:
        unique_together = ("event", "fan", "role")


class Badge(BaseModel):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    badge_name = models.CharField(max_length=32, blank=False)
    rlug_name = models.CharField(max_length=32, blank=False)
    locality = models.CharField(max_length=32, blank=False)
    region = models.CharField(max_length=32, blank=False)
    date_ordered = models.DateField(verbose_name='Date Ordered', null=True)


class ShirtSizesAvailable(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    shirt_size = models.CharField(max_length=8)

    class Meta:
        unique_together = ("event", "shirt_size")


class Shirt(BaseModel):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    shirt_size = models.CharField(max_length=8)

    class Meta:
        unique_together = ("event", "fan")
