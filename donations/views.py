from .models import Donations
from django.views.generic.list import ListView


# Create your views here.


class DonationsListView(ListView):
    queryset = Donations.objects.filter(
        is_public=True).order_by('-event', 'fan')
    template_name = 'donations/donations_list.html'
