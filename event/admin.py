from django.contrib import admin

from .models import Activity, Announcement, Event, Location, Space, Schedule


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'signup_required', 'min_people', 'max_people')
    search_fields = ('title', 'description', 'rules')


admin.site.register(Activity, ActivityAdmin)


class AnnouncementsInLine(admin.TabularInline):
    model = Announcement
    extra = 0


class EventAdmin(admin.ModelAdmin):
    # List display for the admin
    inlines = (AnnouncementsInLine, )
    list_display = ('title', 'start_date', 'end_date', 'theme', 'hashtag')


admin.site.register(Event, EventAdmin)


class LocationAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('name', 'street', 'locality',
                    'region', 'postal_code', 'country')
    list_filter = ('region', 'locality')
    search_fields = ('name', 'street')


admin.site.register(Location, LocationAdmin)


class SpaceAdmin(admin.ModelAdmin):
    # List display for the admin
    list_filter = ('location',)
    list_display = ('location', 'name', 'max_seating')
    search_fields = ('location__name', 'name', 'description')


admin.site.register(Space, SpaceAdmin)


class ScheduleAdmin(admin.ModelAdmin):
    # List display for the admin
    list_filter = ('event', 'space', 'date')
    list_display = ('event', 'is_public', 'activity', 'space',
                    'date', 'start_time', 'end_time')
    list_display_links = ('activity',)
    search_fields = ('activity__title',)


admin.site.register(Schedule, ScheduleAdmin)
