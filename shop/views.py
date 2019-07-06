import datetime
import json
import urllib.error
import urllib.parse
import urllib.request
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.utils.html import format_html
from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView

from event.models import Event
from shop.utils import check_recaptcha
from .cart import ShoppingCart
from .forms import CartItemForm
from .models import Product, Order, OrderItem
from .utils import add_attendee_fan_badge_shirt


# Create your views here.


class EventListView(ListView):
    queryset = Event.objects.all().order_by('start_date').filter(
        start_date__gt=datetime.date.today())
    template_name = 'shop/event_list.html'


class EventProductView(View):
    def get(self, request, event_id):
        obj_products = Product.objects.filter(
            event__id__exact=event_id, is_public=True).order_by('product_type').extra(
            select={'is_top': "product_type = '" + Product.EXHIBITION + "'"})
        date_two_weeks = datetime.date.today() + datetime.timedelta(days=14)
        if obj_products.first().event.start_date <= date_two_weeks:
            obj_products = obj_products.extra(
                order_by=['-is_top', 'product_type'])
        return render(request,
                      'shop/product_list.html',
                      {'object_list': obj_products, 'first': obj_products.first()})


class CartTestView(View):

    def get(self, request):
        str_checkout_id = request.GET.get('checkoutId', None)
        str_reference_id = request.GET.get('referenceId', None)
        if str_reference_id:
            request.session['cart_id'] = str_reference_id
        if str_checkout_id:
            request.session['checkout_id'] = str_checkout_id
        obj_cart = ShoppingCart(request)

        return render(request, 'shop/cart_contents.html', {'error_message': obj_cart.get_debug(request),
                                                           'cart': obj_cart.get_basket(),
                                                           'cart_total': obj_cart.total()})


class CartCheckoutView(View):

    def get(self, request):
        list_message = list()
        obj_cart = ShoppingCart(request)
        str_checkout_id = request.GET.get('checkoutId', "INVALID")
        str_reference_id = request.GET.get('referenceId', "INVALID")
        str_transaction_id = request.GET.get('transactionId', "INVALID")
        if obj_cart.check_checkout_id(str_checkout_id):
            # valid save everything in the users
            obj_order = None
            obj_basket = obj_cart.get_basket()
            for obj_item in obj_basket:
                obj_user = None
                try:
                    obj_user = User.objects.get(email=obj_item.email)
                    list_message.append(
                        "Found existing customer information " + obj_item.email + ".")
                except User.DoesNotExist:
                    obj_user = User.objects.create_user(username=obj_item.email,
                                                        email=obj_item.email,
                                                        first_name=obj_item.first_name,
                                                        last_name=obj_item.last_name,
                                                        password=uuid.uuid4())
                    list_message.append(
                        "Created a user for " + obj_item.email + ". Please check your email for password instructions.")
                    send_mail(subject="Brick Fiesta - New Account Created",
                              message=loader.render_to_string(
                                  "afol/new_account_email.html"),
                              from_email=settings.DEFAULT_FROM_EMAIL,
                              recipient_list=[obj_item.email])
                if obj_order is None:
                    if request.user.is_authenticated:
                        obj_order = Order(user=request.user,
                                          transaction_id=str_transaction_id,
                                          reference_id=str_reference_id,
                                          guest="")
                    else:
                        obj_order = Order(user=obj_user,
                                          transaction_id=str_transaction_id,
                                          reference_id=str_reference_id,
                                          guest="")
                    obj_order.save()
                    list_message.append(
                        "Order associated with " + obj_item.email + ".")
                obj_order_item = OrderItem(order=obj_order,
                                           user=obj_user,
                                           first_name=obj_item.first_name,
                                           last_name=obj_item.last_name,
                                           product=obj_item.product,
                                           price=obj_item.product.price)
                # if obj_item.product.quantity_available > 0:
                #    obj_product = obj_item.product
                #    obj_product.quantity_available -= 1
                #    obj_product.save()
                obj_order_item.save()
                list_message.append(
                    "Order item " + obj_order_item.product.title + " associated with " + obj_item.email + ".")
                add_attendee_fan_badge_shirt(request, obj_order_item)

            obj_cart.clear()
        else:
            list_message.append(
                "It looks like there was an problem with your cart and processing it.")
            list_message.append(
                "We have gathered the data and have sent an email to look into the issue.")
            list_message.append(
                "If you do not hear back in a few days please contact us using the contact form.")

            str_body = "JSON: " + obj_cart.get_debug(request) + "\n\nReference: " + str_reference_id + \
                "\n\nTransaction: " + str_transaction_id
            email = EmailMessage(
                'Brick Fiesta - URGENT - Cart Error', str_body, to=[settings.DEFAULT_FROM_EMAIL])
            email.send()
            obj_cart.clear()

        return render(request, 'shop/cart_complete.html', {'message': list_message, })


class CartView(View):

    def post(self, request, *args, **kwargs):
        str_error_message = False
        obj_cart = ShoppingCart(request)
        if 'cart_item' in request.POST:
            obj_cart.remove(request.POST['cart_item'])
        if 'cart' in request.POST:
            # generate json objects
            str_json = obj_cart.get_json()
            str_json = str_json.encode('utf-8')
            print(str_json)
            str_url = "https://connect.squareup.com/v2/locations/" + \
                settings.SQUARE_LOCATION_KEY + "/checkouts"
            # send request for objects
            obj_request = urllib.request.Request(url=str_url)
            obj_request.add_header(
                'Authorization', 'Bearer ' + settings.SQUARE_CART_KEY)
            obj_request.add_header(
                'Content-Type', 'application/json; charset=utf-8')
            obj_request.add_header('Accept', 'application/json')
            # get response
            obj_response = ""
            try:
                obj_response = urllib.request.urlopen(
                    obj_request, data=str_json)
            except urllib.error.URLError as obj_error:
                # print(obj_error.reason)
                str_error_message = "Unable to reach payment server. Please try again later."
                str_body = "URL: " + str_url + "\n\nJSON: " + \
                    str_json.decode('ascii') + "\n\nRESPONSE:" + obj_response
                email = EmailMessage(
                    'Brick Fiesta - Check Out URL Error', str_body, to=[settings.DEFAULT_FROM_EMAIL])
                email.send()
                pass
            except urllib.error.HTTPError as obj_error:
                str_error_message = "Unable to process payment correctly. Error sent to event organizers."
                str_body = "URL: " + str_url + "\n\nJSON: " + \
                    str_json.decode('ascii') + "\n\nRESPONSE:" + obj_response
                email = EmailMessage(
                    'Brick Fiesta - Check Out HTTP Error', str_body, to=[settings.DEFAULT_FROM_EMAIL])
                email.send()
                # print(obj_error.code)
                # print(obj_error.read())
                pass
            else:
                result = json.loads(obj_response.read().decode())
                # print(result)
                obj_cart.set_checkout_id(request, result['checkout']['id'])
                return redirect(result['checkout']['checkout_page_url'])

        return render(request, 'shop/cart_contents.html', {'error_message': str_error_message,
                                                           'cart': obj_cart.get_basket(),
                                                           'cart_total': obj_cart.total()})

    def get(self, request, token=None):
        if token:
            request.session['cart'] = str(token)
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
        if not check_recaptcha(request):
            form.add_error(
                None, 'You failed the human test. Try the reCAPTCHA again.')

        if form.is_valid():
            cart.add(first_name=form.cleaned_data['first_name'],
                     last_name=form.cleaned_data['last_name'],
                     email=form.cleaned_data['email'],
                     product=self.object)
            messages.info(request, format_html(
                'Product added to <a href="{}">cart</a>.', reverse('shop:cart')))
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
