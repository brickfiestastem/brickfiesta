from django.contrib import admin
from .models import Activity, Event, Location, Space

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'signup_required', 'min_people', 'max_people')

admin.site.register(Activity, ActivityAdmin)

class EventAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('title', 'start_date', 'end_date', 'theme', 'hashtag')

admin.site.register(Event, EventAdmin)

class LocationAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('name', 'street', 'locality', 'region', 'postal_code', 'country')

admin.site.register(Location, LocationAdmin)


class SpaceAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('location', 'name', 'max_seating')

admin.site.register(Space, SpaceAdmin)
