from django.shortcuts import render, get_object_or_404
from event.models import Event, Location



def index(request):
    obj_events = Event.objects.all().order_by('start_date')
    return render(request, 'event/index.html', {'events': obj_events})

def details(request, event_id):
    obj_event = get_object_or_404(Event, id=event_id)
    return render(request, 'event/details.html', {'event': obj_event})

def locations(request):
    obj_locations = Location.objects.all().order_by('postal_code')
    return render(request, 'event/locations.html', {'locations': obj_locations})

def location(request, location_id):
    obj_location = get_object_or_404(Location, id=location_id)
    return render(request, 'event/location.html', {'location': obj_location})