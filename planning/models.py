from django.db import models
from event.models import Event
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class InventoryItem(BaseModel):
    make = models.CharField(verbose_name='Make', max_length=64)
    model = models.CharField(verbose_name='Model', max_length=64)
    description = models.TextField(verbose_name='Description')
    serial_number = models.CharField(
        verbose_name='Serial Number', max_length=64)
    purchase_price = models.FloatField(verbose_name='Purchase Price')
    purchase_date = models.DateField(verbose_name='Date of Purchase')
    status = models.TextField(verbose_name='Status', max_length=64)
    condition = models.TextField(verbose_name='Condition', max_length=64)
    event = models.ForeignKey(Event, on_delete=None)
    # user = models.ForeignKey(User, on_delete=None)