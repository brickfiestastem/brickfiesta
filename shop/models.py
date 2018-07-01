import uuid

from django.contrib.auth.models import User
from django.db import models

from event.models import Event
from referral.models import Referral
from shop.utils import upload_path_product


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class ProductManager(models.Manager):
    def get_product_bullets(self, product_uuid):
        if isinstance(product_uuid, str):
            product_uuid = uuid.UUID(product_uuid)
        return self.get(id=product_uuid).productbulletpoint_set.all()


class Product(BaseModel):
    CONVENTION = 'convention'
    EXHIBITION = 'exhibition'
    SPONSORSHIP = 'sponsor'
    VENDOR = 'vendor'


    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    PRODUCT_TYPE = (
        (CONVENTION, 'Fan Convention'),
        (EXHIBITION, 'Public Exhibition'),
        (SPONSORSHIP, 'Sponsorship'),
        (VENDOR, 'Vendor'),
    )
    product_type = models.CharField(
        max_length=64, blank=False, choices=PRODUCT_TYPE, default='convention')
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to=upload_path_product, null=True)
    quantity_available = models.IntegerField(
        verbose_name='Quantity Available', default=-1)
    has_tshirt = models.BooleanField(
        verbose_name="Has T-Shirt?", default=False)
    has_badge = models.BooleanField(verbose_name="Has Badge?", default=False)
    is_public = models.BooleanField(
        verbose_name="Is Public on Site?", default=True)
    objects = ProductManager()

    class Meta:
        ordering = ['product_type', 'title']
        unique_together = ('title', 'event')

    def __str__(self):
        return self.event.title + " - " + self.title


class ProductBulletPoint(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.CharField(max_length=64, blank=True)


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(
        max_length=128, null=True, default=uuid.uuid4)
    reference_id = models.CharField(
        max_length=128, null=True, default=uuid.uuid4)
    guest = models.CharField(max_length=255, default="N/A")
    referral = models.ForeignKey(
        Referral, on_delete=None, blank=True, null=True)

    def __str__(self):
        return self.reference_id + " on " + str(self.created)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()


class CartItem(BaseModel):
    cart = models.CharField(max_length=64, default=uuid.uuid4)
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
