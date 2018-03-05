from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import View, TemplateView
from .models import Business, Vendor, Sponsor
from event.models import Event
from shop.models import Product
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import SponsorForm, VendorForm
from shop.utils import check_recaptcha
import datetime


class UpcomingView(TemplateView):
    template_name = 'vendor/business_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()
        obj_events_upcoming = Event.objects.all().order_by(
            'start_date').filter(start_date__gt=today)
        context['sponsor_list'] = Sponsor.objects.all().order_by(
            'business').filter(event__in=obj_events_upcoming)
        context['vendor_list'] = Vendor.objects.all().order_by(
            'business').filter(event__in=obj_events_upcoming)
        return context


class SponsorListView(ListView):
    queryset = Sponsor.objects.all()
    template_name = 'vendor/sponsor_list.html'


class VendorListView(ListView):
    queryset = Vendor.objects.all()
    template_name = 'vendor/vendor_list.html'


class BusinessDetail(DetailView):
    model = Business

    def get_context_data(self, **kwargs):
        context = super(BusinessDetail, self).get_context_data(**kwargs)
        context['business_owner'] = (
            self.object.user.id == self.request.user.id)
        return context


class VendorRequestDetail(View):
    template_name = 'vendor/vendor_request.html'

    def get(self, request, *args, **kwargs):
        today = datetime.date.today()
        step_one_signed_in = self.request.user.is_authenticated
        step_two_business = False
        business_id = None
        if step_one_signed_in:
            step_two_business = Business.objects.filter(
                user=self.request.user.id).exists()
        if step_two_business:
            business_id = Business.objects.filter(
                user=self.request.user.id).first()
        step_three_register = False
        if step_two_business:
            step_three_register = Product.objects.all().order_by(
                'event__start_date').filter(event__start_date__gt=today, product_type='vendor').exists()
        form = None
        if step_three_register:
            form = VendorForm()
        step_four_status = False
        if step_one_signed_in:
            step_four_status = Vendor.objects.filter(user=self.request.user.id)

        return render(request, self.template_name, {'step_one_signed_in': step_one_signed_in,
                                                    'step_two_business': step_two_business,
                                                    'step_three_register': step_three_register,
                                                    'step_four_status': step_four_status,
                                                    'form': form,
                                                    'business_id': business_id})

    def post(self, request, *args, **kwargs):
        today = datetime.date.today()
        step_one_signed_in = self.request.user.is_authenticated
        step_two_business = False
        business_id = None
        if step_one_signed_in:
            step_two_business = Business.objects.filter(
                user=self.request.user.id).exists()
        if step_two_business:
            business_id = Business.objects.filter(
                user=self.request.user.id).first()
        step_three_register = False
        if step_two_business:
            step_three_register = Product.objects.all().order_by('event__start_date').filter(
                event__start_date__gt=today, product_type='vendor').exists()
        form = VendorForm(request.POST)
        if form.is_valid():
            if not check_recaptcha(request):
                form.add_error(
                    None, 'You failed the human test. Try the reCAPTCHA again.')
            else:
                obj_product = Product.objects.get(id=request.POST['product'])
                obj_event = obj_product.event
                if not Vendor.objects.filter(event=obj_event, business=business_id).exists():
                    form.instance.user = self.request.user
                    form.instance.event = obj_event
                    form.instance.business = business_id
                    form.save()
                else:
                    form.add_error(
                        'product', 'Already submitted request for this event.')
        step_four_status = False
        if step_one_signed_in:
            step_four_status = Vendor.objects.filter(user=self.request.user.id)

        return render(request, self.template_name, {'step_one_signed_in': step_one_signed_in,
                                                    'step_two_business': step_two_business,
                                                    'step_three_register': step_three_register,
                                                    'step_four_status': step_four_status,
                                                    'form': form,
                                                    'business_id': business_id})


class SponsorRequestDetail(View):
    # TODO: refactor vendor and sponsor to use the same abstract
    template_name = 'vendor/sponsor_request.html'

    def get(self, request, *args, **kwargs):
        today = datetime.date.today()
        step_one_signed_in = self.request.user.is_authenticated
        step_two_business = False
        business_id = None
        if step_one_signed_in:
            step_two_business = Business.objects.filter(
                user=self.request.user.id).exists()
        if step_two_business:
            business_id = Business.objects.filter(
                user=self.request.user.id).first()
        step_three_register = False
        if step_two_business:
            step_three_register = Product.objects.filter(
                product_type='sponsor', event__start_date__gt=today).order_by(
                    'event__start_date').exists()
        form = None
        if step_three_register:
            form = SponsorForm()
        step_four_status = False
        if step_one_signed_in:
            step_four_status = Sponsor.objects.filter(
                user=self.request.user.id)

        return render(request, self.template_name, {'step_one_signed_in': step_one_signed_in,
                                                    'step_two_business': step_two_business,
                                                    'step_three_register': step_three_register,
                                                    'step_four_status': step_four_status,
                                                    'form': form,
                                                    'business_id': business_id})

    def post(self, request, *args, **kwargs):
        today = datetime.date.today()
        step_one_signed_in = self.request.user.is_authenticated
        step_two_business = False
        business_id = None
        if step_one_signed_in:
            step_two_business = Business.objects.filter(
                user=self.request.user.id).exists()
        if step_two_business:
            business_id = Business.objects.filter(
                user=self.request.user.id).first()
        step_three_register = False
        if step_two_business:
            step_three_register = Product.objects.filter(
                product_type='sponsor', event__start_date__gt=today).order_by(
                    'event__start_date').exists()
        form = SponsorForm(request.POST)
        if form.is_valid():
            if not check_recaptcha(request):
                form.add_error(
                    None, 'You failed the human test. Try the reCAPTCHA again.')
            else:
                obj_product = Product.objects.get(id=request.POST['product'])
                obj_event = obj_product.event
                if not Sponsor.objects.filter(event=obj_event, business=business_id).exists():
                    form.instance.user = self.request.user
                    form.instance.event = obj_event
                    form.instance.business = business_id
                    form.instance.product_quantity = 1
                    form.save()
                else:
                    form.add_error(
                        'product', 'Already submitted request for this event.')
        step_four_status = False
        if step_one_signed_in:
            step_four_status = Sponsor.objects.filter(
                user=self.request.user.id)

        return render(request, self.template_name, {'step_one_signed_in': step_one_signed_in,
                                                    'step_two_business': step_two_business,
                                                    'step_three_register': step_three_register,
                                                    'step_four_status': step_four_status,
                                                    'form': form,
                                                    'business_id': business_id})


@method_decorator(login_required, name='dispatch')
class BusinessAddView(CreateView):
    model = Business
    fields = ('name', 'description', 'street', 'locality',
              'region', 'postal_code', 'country', 'phone_number',
              'url', 'logo')
    success_url = '/vendor/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not check_recaptcha(self.request):
            form.add_error(
                None, 'You failed the human test. Try the reCAPTCHA again.')
            return super().form_invalid(form)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class BusinessUpdateView(UpdateView):
    model = Business
    fields = ('name', 'description', 'street', 'locality',
              'region', 'postal_code', 'country', 'phone_number',
              'url', 'logo')
    success_url = '/afol/profile/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not check_recaptcha(self.request):
            form.add_error(
                None, 'You failed the human test. Try the reCAPTCHA again.')
            return super().form_invalid(form)
        return super().form_valid(form)
