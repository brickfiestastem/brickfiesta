from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Business, Vendor, Sponsor
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class SponsorListView(ListView):
    queryset = Sponsor.objects.all()
    template_name = 'vendor/vendor_list.html'


class VendorListView(ListView):
    queryset = Vendor.objects.all()
    template_name = 'vendor/vendor_list.html'


class BusinessDetail(DetailView):
    model = Business


@method_decorator(login_required, name='dispatch')
class BusinessAddView(CreateView):
    model = Business
    fields = ('name', 'description', 'street', 'locality',
              'region', 'postal_code', 'country', 'phone_number',
              'url', 'logo')
    success_url = '/vendor/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class BusinessUpdateView(UpdateView):
    model = Business
    fields = ('name', 'description', 'street', 'locality',
              'region', 'postal_code', 'country', 'phone_number',
              'url', 'logo')
    success_url = '/vendor/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)