import uuid

from django.db import models

from event.models import Event, Activity
from shop.models import Product


# from django.conf import settings


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class Program(BaseModel):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    welcome_message = models.TextField(
        verbose_name='Welcome Message', default='')
    closing_remarks = models.TextField(
        verbose_name='Closing Remarks', default='')
    disclaimer = models.TextField(verbose_name='Disclaimer',
                                  default='Brick Fiesta is generously sponsored by Alamo, Inc, '
                                          'a 501(c)3 non-profit corporation. LEGO (r) is a '
                                          'registered trademark of The LEGO Group, which does not sponsor, '
                                          'authorize, or endorse this event or website.')
    volunteer_thanks = models.TextField(verbose_name='Volunteer Thanks',
                                        default='Thank you to all our sponsor, vendors, members, '
                                                'and volunteers. Without you we would not have been '
                                                'able to have such an awesome event!')


class ProgramContributors(BaseModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title of Person', max_length=128)
    name = models.CharField(verbose_name='Name of Person', max_length=128)
    order = models.IntegerField(verbose_name='Order of Display', default=0)


class ProgramHighlightActivity(BaseModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)


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
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None)


class BagCheckListItems(BaseModel):
    product = models.ForeignKey(Product, models.CASCADE)
    item = models.CharField(verbose_name='Additional Item', max_length=64)

    class Meta:
        ordering = ['product', 'item']
        verbose_name_plural = 'Bag Items'
