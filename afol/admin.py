from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Attendee, Badge, Profile, Shirt


class AttendeeAdmin(admin.ModelAdmin):
    ordering = ("event__title", "user__last_name", "user__first_name")
    list_filter = ("event", "role")
    list_display = ('event', 'user', 'role')
    list_display_links = ('role', )


admin.site.register(Attendee, AttendeeAdmin)


class BadgeAdmin(admin.ModelAdmin):
    list_filter = ("event", )
    list_display = ('event', 'user', 'badge_name', 'date_ordered')


admin.site.register(Badge, BadgeAdmin)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class ShirtAdmin(admin.ModelAdmin):
    list_filter = ('event', 'shirt_size')
    list_display = ('event', 'user', 'shirt_size')


admin.site.register(Shirt, ShirtAdmin)
