from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Attendee, Badge, User, Shirt
from django.contrib.auth.models import User


class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'role')


admin.site.register(Attendee, AttendeeAdmin)


class BadgeAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'badge_name', 'date_ordered')


admin.site.register(Badge, BadgeAdmin)


class ProfileAdmin(UserAdmin):
    list_display = ('user', 'bricklink_username',
                    'twitter_handle', 'flickr_handle')


admin.site.register(User, ProfileAdmin)


class ShirtAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'shirt_size')


admin.site.register(Shirt, ShirtAdmin)
