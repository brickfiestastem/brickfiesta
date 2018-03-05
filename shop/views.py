from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView, FormView
from event.models import Event
from .models import Product
from .forms import CartItemForm
from .cart import ShoppingCart
import datetime

# Create your views here.


class EventListView(ListView):
    queryset = Event.objects.all().order_by('start_date').filter(
        start_date__gt=datetime.date.today())
    template_name = 'shop/event_list.html'


class EventProductView(View):
    def get(self, request, event_id):
        obj_products = Product.objects.filter(event__id__exact=event_id)
        return render(request,
                      'shop/product_list.html',
                      {'object_list': obj_products, 'first': obj_products.first()})


class CartView(View):

    def post(self, request, *args, **kwargs):
        # TODO Process checkout
        # TODO Process remove
        obj_cart = ShoppingCart(request)
        if 'cart_item' in request.POST:
            obj_cart.remove(request.POST['cart_item'])
        return render(request, 'shop/cart_contents.html', {'cart': obj_cart.get_basket(),
                                                           'cart_total': obj_cart.total()})

    def get(self, request):
        obj_cart = ShoppingCart(request)
        return render(request, 'shop/cart_contents.html', {'cart': obj_cart.get_basket(),
                                                           'cart_total': obj_cart.total()})


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = CartItemForm()
        return context


class ProductCartItemView(SingleObjectMixin, FormView):
    template_name = 'shop/product_detail.html'
    form_class = CartItemForm
    model = Product

    def post(self, request, *args, **kwargs):
        cart = ShoppingCart(request)
        self.object = self.get_object()
        form = CartItemForm(request.POST)
        if form.is_valid():
            cart.add(first_name=form.cleaned_data['first_name'],
                     last_name=form.cleaned_data['last_name'],
                     email=form.cleaned_data['email'],
                     product=self.object)
        return super(ProductCartItemView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('shop:event', kwargs={'event_id': self.object.event.id})


class ProductDetail(View):
    def get(self, request, *args, **kwargs):
        view = ProductDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProductCartItemView.as_view()
        return view(request, *args, **kwargs)
