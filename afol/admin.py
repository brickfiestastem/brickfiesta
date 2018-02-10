from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Attendee, Badge, User, Shirt
from .forms import AfolUserChangeForm, AfolUserCreateForm


class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'role')


admin.site.register(Attendee, AttendeeAdmin)


class BadgeAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'badge_name', 'date_ordered')


admin.site.register(Badge, BadgeAdmin)


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = AfolUserCreateForm
    form = AfolUserChangeForm


admin.site.register(User, CustomUserAdmin)


class ShirtAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'shirt_size')


admin.site.register(Shirt, ShirtAdmin)
