from django.db.models import Sum
from .models import CartItem
from django.conf import settings
import json
import uuid


class ShoppingCart(object):

    def __init__(self, request):
        self.cart_id = request.session.get('cart', str(uuid.uuid4()))
        request.session['cart'] = self.cart_id
        self.host_url = request.session.get('host_url', request.get_host())
        request.session['host_url'] = self.host_url
        self.checkout_key = request.session.get('checkout_key', str(uuid.uuid4()))
        request.session['checkout_key'] = self.checkout_key

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
        total['product__price__sum'] = 0.0
        if CartItem.objects.filter(cart=self.cart_id).exists():
            total = CartItem.objects.filter(
                cart=self.cart_id).aggregate(Sum('product__price'))
        return total['product__price__sum']

    def get_basket(self):
        return CartItem.objects.filter(cart=self.cart_id)

    def get_json(self):
        str_json = dict()
        str_json['idempotency_key'] = str(uuid.uuid4())
        str_json['merchant_support_email'] = settings.DEFAULT_FROM_EMAIL
        cart_items = CartItem.objects.filter(cart=self.cart_id).prefetch_related('product')
        str_order = dict()
        str_order['reference_id'] = str(self.cart_id)
        str_line_items = list()
        for cart_item in cart_items:
            str_item = dict()
            str_item['name'] = str(cart_item.product.title)
            str_item['quantity'] = "1"
            str_base_price_money = dict()
            str_base_price_money['amount'] = int(round(cart_item.product.price * 100))
            str_base_price_money['currency'] = "USD"
            str_item['base_price_money'] = str_base_price_money
            str_line_items.append(str_item)
        # str_taxes = dict()
        # str_taxes['name'] = "Sales Tax (TX)"
        # str_taxes['percentage'] = "8.125"
        # str_taxes['type'] = "ADDITIVE"
        # str_line_items.append(str_taxes)
        str_order['line_items'] = str_line_items
        str_json['order'] = str_order
        str_json['redirect_url'] = "https://" + self.host_url + "/shop/cartcheckout/" + self.checkout_key
        return json.dumps(str_json)

    def check_key(self, str_key):
        return str_key == self.checkout_key
