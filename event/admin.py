from django.contrib import admin
from .models import Activity, Event, Location, Space, Schedule


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'signup_required', 'min_people', 'max_people')


admin.site.register(Activity, ActivityAdmin)


class EventAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('title', 'start_date', 'end_date', 'theme', 'hashtag')


admin.site.register(Event, EventAdmin)


class LocationAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('name', 'street', 'locality',
                    'region', 'postal_code', 'country')


admin.site.register(Location, LocationAdmin)


class SpaceAdmin(admin.ModelAdmin):
    # List display for the admin
    list_filter = ('location',)
    list_display = ('location', 'name', 'max_seating')


admin.site.register(Space, SpaceAdmin)


class ScheduleAdmin(admin.ModelAdmin):
    # List display for the admin
    list_filter = ('event', 'space', 'date')
    list_display = ('event', 'activity', 'space',
                    'date', 'start_time', 'end_time')


admin.site.register(Schedule, ScheduleAdmin)
