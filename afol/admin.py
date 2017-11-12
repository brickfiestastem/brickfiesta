from django.contrib import admin
from .models import Attendee, Badge, Profile, Shirt


class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'role')


admin.site.register(Attendee, AttendeeAdmin)


class BadgeAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'badge_name', 'date_ordered')


admin.site.register(Badge, BadgeAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bricklink_username',
                    'twitter_handle', 'flickr_handle')


admin.site.register(Profile, ProfileAdmin)


class ShirtAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'shirt_size')


admin.site.register(Shirt, ShirtAdmin)
