from django import forms
from .models import Sponsor, Vendor
from shop.models import Product
import datetime


class VendorForm(forms.ModelForm):
    today = datetime.date.today()
    product = forms.ModelChoiceField(
        queryset=Product.objects.all().order_by('event__start_date').filter(event__start_date__gt=today,
                                                                            product_type='vendor'))

    class Meta:
        model = Vendor
        fields = ('product', 'product_quantity',)


class SponsorForm(forms.ModelForm):
    today = datetime.date.today()
    product = forms.ModelChoiceField(
        queryset=Product.objects.all().order_by('event__start_date').filter(event__start_date__gt=today,
                                                                            product_type='sponsor'))

    class Meta:
        model = Sponsor
        fields = ('product',)
