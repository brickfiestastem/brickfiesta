from django.shortcuts import render, get_object_or_404
from event.models import Event, Location


def locations(request):
    obj_locations = Location.objects.all().order_by('postal_code')
    return render(request, 'event/locations.html', {'locations': obj_locations})

def location(request, location_id):
    obj_location = get_object_or_404(Location, id=location_id)
    return render(request, 'event/location.html', {'location': obj_location})