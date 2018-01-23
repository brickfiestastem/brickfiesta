from django.db import models
from django.contrib.auth.models import User
from event.models import Event
from event.utils import upload_path_product
from referral.models import Referral
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class ProductType(BaseModel):
    title = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.title


class Product(BaseModel):
    event = models.ForeignKey(Event, on_delete=None)
    product_type = models.ForeignKey(ProductType, on_delete=None)
    title = models.CharField(max_length=64)
    description = models.TextField()
    bullet_point_one = models.CharField(max_length=64, blank=True)
    bullet_point_two = models.CharField(max_length=64, blank=True)
    bullet_point_three = models.CharField(max_length=64, blank=True)
    bullet_point_four = models.CharField(max_length=64, blank=True)
    bullet_point_five = models.CharField(max_length=64, blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to=upload_path_product, null=True)


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=None)
    guest = models.CharField(max_length=255)
    referral = models.ForeignKey(Referral, on_delete=None)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=None)
    user = models.ForeignKey(User, on_delete=None, null=True)
    product = models.ForeignKey(Product, on_delete=None)
    price = models.FloatField()


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=None, null=True)
    session = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.session


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=None)
    first_name = models.CharField(max_length=16, blank=True)
    last_name = models.CharField(max_length=16, blank=True)
    email = models.EmailField(blank=True)
    product = models.ForeignKey(Product, on_delete=None)
