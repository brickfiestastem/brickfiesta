from django.views.generic.list import ListView
from django.views.generic import DetailView
from .models import Business, Vendor, Sponsor


class SponsorListView(ListView):
    queryset = Sponsor.objects.all()
    template_name = 'vendor/vendor_list.html'


class VendorListView(ListView):
    queryset = Vendor.objects.all()
    template_name = 'vendor/vendor_list.html'


class VendorDetail(DetailView):
    model = Business
