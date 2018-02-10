from django.shortcuts import render
from event.models import Event, Location
from vendor.models import Sponsor, Vendor
from django.views.generic import DetailView
import datetime


def frontpage(request):
    today = datetime.date.today()
    obj_events_current = Event.objects.all().order_by(
        '-start_date').filter(start_date__lte=today, end_date__gte=today)
    obj_events_upcoming = Event.objects.all().order_by(
        'start_date').filter(start_date__gt=today)
    obj_events_past = Event.objects.all().order_by(
        '-start_date').filter(end_date__lt=today)
    obj_sponsors = Sponsor.objects.all().order_by(
        'business').filter(event__in=obj_events_upcoming)
    obj_vendors = Vendor.objects.all().order_by(
        'business').filter(event__in=obj_events_upcoming)

    return render(request, 'event/frontpage.html', {'events_current': obj_events_current,
                                                    'events_upcoming': obj_events_upcoming,
                                                    'events_past': obj_events_past,
                                                    'sponsor_list': obj_sponsors,
                                                    'vendor_list': obj_vendors})


class EventDetail(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['sponsor_list'] = Sponsor.objects.filter(
            event=self.object, status='approved')
        context['vendor_list'] = Vendor.objects.filter(
            event=self.object, status='approved')
        return context


class LocationDetail(DetailView):
    model = Location
