from django.db.models import Sum
from .models import CartItem
import uuid


class ShoppingCart(object):

    def __init__(self, request):
        self.cart_id = request.session.get('cart', str(uuid.uuid4()))
        request.session['cart'] = self.cart_id

    def add(self,  first_name, last_name, email, product):
        basket_item, created = CartItem.objects.get_or_create(cart=self.cart_id,
                                                              first_name=first_name,
                                                              last_name=last_name,
                                                              email=email,
                                                              product=product)
        return created

    def remove(self, cart_item):
        basket_item = CartItem.objects.get(id=cart_item)
        basket_item.delete()

    def clear(self):
        CartItem.objects.filter(cart=self.cart_id).delete()

    def __len__(self):
        return CartItem.objects.filter(cart=self.cart_id).count()

    def total(self):
        total = dict()
        total['product__price__sum'] = 0
        if CartItem.objects.filter(cart=self.cart_id).exists:
            total = CartItem.objects.filter(cart=self.cart_id).aggregate(Sum('product__price'))
        return total['product__price__sum']

    def get_basket(self):
        return CartItem.objects.filter(cart=self.cart_id)
