from django.contrib import admin
from django.utils.html import mark_safe

from afol.models import ScheduleAttendee, ScheduleVolunteer
from .models import Activity, Announcement, Event, Location, Space, Schedule


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'signup_required', 'min_people', 'max_people')
    search_fields = ('title', 'description', 'rules')
    readonly_fields = ['picture_image', ]

    def picture_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.picture.url,
            width=obj.picture.width,
            height=obj.picture.height,
        )
        )


admin.site.register(Activity, ActivityAdmin)


class AnnouncementsInLine(admin.TabularInline):
    model = Announcement
    extra = 0


class EventAdmin(admin.ModelAdmin):
    # List display for the admin
    inlines = (AnnouncementsInLine, )
    list_display = ('title', 'start_date', 'end_date', 'theme', 'hashtag')

    readonly_fields = ['logo_image', ]

    def logo_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.logo.url,
            width=obj.logo.width,
            height=obj.logo.height,
        ))


admin.site.register(Event, EventAdmin)


class LocationAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('name', 'street', 'locality',
                    'region', 'postal_code', 'country')
    list_filter = ('region', 'locality')
    search_fields = ('name', 'street')

    readonly_fields = ['map_image', ]

    def map_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.map.url,
            width=obj.map.width,
            height=obj.map.height,
        )
        )


admin.site.register(Location, LocationAdmin)


class SpaceAdmin(admin.ModelAdmin):
    # List display for the admin
    list_filter = ('location',)
    list_display = ('location', 'name', 'max_seating')
    search_fields = ('location__name', 'name', 'description')

    readonly_fields = ['map_image', ]

    def map_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.map.url,
            width=obj.map.width,
            height=obj.map.height,
        ))


admin.site.register(Space, SpaceAdmin)


class ScheduleAttendeeInLine(admin.TabularInline):
    model = ScheduleAttendee
    extra = 0


class ScheduleVolunteerInLine(admin.TabularInline):
    model = ScheduleVolunteer
    extra = 0


class ScheduleAdmin(admin.ModelAdmin):
    # List display for the admin

    def attendee_count(self, obj):
        return obj.scheduleattendee_set.count()

    attendee_count.short_description = "Attendees"

    def volunteer_count(self, obj):
        return obj.schedulevolunteer_set.count()

    volunteer_count.short_description = "Volunteers"

    inlines = (ScheduleVolunteerInLine, ScheduleAttendeeInLine)
    list_filter = ('event', 'space', 'date')
    list_display = ('activity', 'date', 'start_time', 'end_time',
                    'space', 'volunteer_count', 'attendee_count',
                    'is_public', 'is_printable', 'event', )
    list_display_links = ('activity',)
    search_fields = ('activity__title',)


admin.site.register(Schedule, ScheduleAdmin)
