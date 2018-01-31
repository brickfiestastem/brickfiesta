from django.shortcuts import render, get_object_or_404
from event.models import Event, Location
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

    return render(request, 'event/frontpage.html', {'events_current': obj_events_current,
                                                    'events_upcoming': obj_events_upcoming,
                                                    'events_past': obj_events_past})


class EventDetail(DetailView):
    model = Event


class LocationDetail(DetailView):
    model = Location
