import uuid
from django.db import models
from django.contrib.auth.models import User
from event.models import Event
from vendor.models import Business
from afol.models import Fan


# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class Donations(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, blank=True, null=True)
    fan = models.ForeignKey(
        Fan, on_delete=models.CASCADE, blank=True, null=True)
    item = models.CharField(verbose_name='Item Donated', max_length=256)
    item_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_public = models.BooleanField(verbose_name='Is Public?', default=True)
    is_price_public = models.BooleanField(
        verbose_name='Is Price Public?', default=False)

    def __str__(self):
        return str(self.event) + " - " + self.item

    class Meta:
        verbose_name_plural = "donations"


class DonationNotes(BaseModel):
    donation = models.ForeignKey(Donations, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField(verbose_name='Note')
