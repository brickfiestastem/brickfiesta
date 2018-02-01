from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from event.models import Event
from .models import Product, Cart, CartItem
import datetime

# Create your views here.


class EventListView(ListView):
    queryset = Event.objects.all().order_by('start_date').filter(
        start_date__gt=datetime.date.today())
    template_name = 'shop/event_list.html'


class EventProductView(View):
    def get(self, request, event_id):
        obj_products = Product.objects.filter(event__id__exact=event_id)
        return render(request, 'shop/product_list.html', {'object_list': obj_products, 'first': obj_products.first()})


class CartView(View):
    def get_cart(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(session=request.session.get('id'))
        return cart

    def get(self, request):
        obj_cart = self.get_cart(request)
        return render(request, 'shop/cart_contents.html', {'cart': obj_cart})

    def post(self, request, *args, **kwargs):
        obj_cart = self.get_cart(request)
        return render(request, 'shop/cart_item_added.html', {'cart': obj_cart})


class Details(View):
    def get(self, request, product_id):
        obj_product = get_object_or_404(Product, id=product_id)
        return render(request, 'shop/product_details.html', {'product': obj_product})

    def post(self, request, product_id, *args, **kwargs):
        post_params = request.POST.dict()
        cart = Cart.objects.get(session=request.session.get('id'))
        obj_product = Product.objects.get(id=post_params.get('product_id'))
        cart_item = CartItem.objects.create(cart=cart,
                                            first_name=post_params.get(
                                                'first'),
                                            last_name=post_params.get('last'),
                                            email=post_params.get('email'),
                                            product=obj_product)

        return render(request, 'shop/product_details.html', {'product': obj_product})
