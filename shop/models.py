from django.db import models
from django.contrib.auth.models import User
from event.models import Event
from shop.utils import upload_path_product
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


class ProductManager(models.Manager):
    def get_product_bullets(self, product_uuid):
        if isinstance(product_uuid, str):
            product_uuid = uuid.UUID(product_uuid)
        return self.get(id=product_uuid).productbulletpoint_set.all()


class Product(BaseModel):
    event = models.ForeignKey(Event, on_delete=None)
    product_type = models.ForeignKey(ProductType, on_delete=None)
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to=upload_path_product, null=True)
    objects = ProductManager()

    def __str__(self):
        return self.event.title + " - " + self.title


class ProductBulletPoint(BaseModel):
    product = models.ForeignKey(Product, on_delete=None)
    text = models.CharField(max_length=64, blank=True)


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
