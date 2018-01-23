from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product, Cart, CartItem

# Create your views here.


def index(request):
    obj_products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': obj_products})


class Cart(View):
    def get(self, request):
        try:
            obj_cart = Cart.objects.get(session=request.session.get('id'))
        except Exception:
            obj_cart = None
        return render(request, 'shop/cart_contents.html', {'cart': obj_cart})


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
