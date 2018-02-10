from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from django.views.generic import DetailView
from event.models import Event
from .models import Business, Vendor, Sponsor
import datetime

# Create your views here.


class VendorListView(ListView):
    queryset = Vendor.objects.all()
    template_name = 'vendor/vendor_list.html'


class VendorDetail(DetailView):
    model = Business
