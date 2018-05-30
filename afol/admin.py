from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Attendee, Badge, Fan, Profile, Shirt
from django.core.mail import send_mail
from django.template import loader
from django.conf import settings
import uuid
from django.contrib import messages


class AttendeeAdmin(admin.ModelAdmin):
    ordering = ("event__title", "fan__last_name", "fan__first_name")
    list_filter = ("event", "role")
    list_display = ('event', 'fan', 'role')
    list_display_links = ('role', )


admin.site.register(Attendee, AttendeeAdmin)


class BadgeAdmin(admin.ModelAdmin):
    list_filter = ("event", )
    list_display = ('event', 'fan', 'badge_name', 'date_ordered')


admin.site.register(Badge, BadgeAdmin)


class FanAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')

admin.site.register(Fan, FanAdmin)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


def fix_order_password(modeladmin, request, queryset):
    for obj_user in queryset:
        obj_user.set_password(uuid.uuid4())
        obj_user.save()
        send_mail(subject="Brick Fiesta - New Account Created",
                  message=loader.render_to_string(
                      "afol/new_account_email.html"),
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[obj_user.email])
        messages.info(request, "Email sent to %s." % obj_user.email)


fix_order_password.short_description = "Fix users password problem"


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    actions = [fix_order_password]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class ShirtAdmin(admin.ModelAdmin):
    list_filter = ('event', 'shirt_size')
    list_display = ('event', 'fan', 'shirt_size')


admin.site.register(Shirt, ShirtAdmin)
