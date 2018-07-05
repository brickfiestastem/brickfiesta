import datetime
import uuid

from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import loader
from django.utils.html import mark_safe

from .models import Attendee, Badge, Fan, Profile, Shirt


class AttendeeAdmin(admin.ModelAdmin):
    ordering = ("event__title", "fan__last_name", "fan__first_name")
    list_filter = ("event", "role")
    list_display = ('event', 'fan', 'role')
    list_display_links = ('role',)
    search_fields = ('fan__last_name', 'fan__first_name')


admin.site.register(Attendee, AttendeeAdmin)


def badge_ordered(modeladmin, request, queryset):
    today = datetime.date.today()
    for obj_badge in queryset:
        obj_badge.date_ordered = today
        obj_badge.save()


badge_ordered.short_description = "Set the date ordered on badge"


class BadgeAdmin(admin.ModelAdmin):
    list_filter = ("event",)
    list_display = ('event', 'fan', 'badge_name', 'date_ordered')
    search_fields = ('fan__last_name', 'fan__first_name',
                     'badge_name', 'date_ordered')
    actions = [badge_ordered]


admin.site.register(Badge, BadgeAdmin)


def generate_barcode(modeladmin, request, queryset):
    for obj_fan in queryset:
        obj_fan.generate_barcode()


generate_barcode.short_description = "Generate barcode"


class FanAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    actions = [generate_barcode]

    readonly_fields = ['barcode_image', ]

    def barcode_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.bar_code.url,
            width=obj.bar_code.width,
            height=obj.bar_code.height,
        )
        )


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
    inlines = (ProfileInline,)
    actions = [fix_order_password]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


def shirt_ordered(modeladmin, request, queryset):
    today = datetime.date.today()
    for obj_shirt in queryset:
        obj_shirt.date_ordered = today
        obj_shirt.save()


shirt_ordered.short_description = "Set the date ordered on shirts"


def shirt_reminder(modeladmin, request, queryset):
    for obj_shirt in queryset:
        obj_user = obj_shirt.fan.user
        str_shirt = str(obj_shirt)
        send_mail(subject="Brick Fiesta - Shirt Size Reminder",
                  message=loader.render_to_string(
                      "afol/shirt_reminder_email.html",
                      {'user_first_name': obj_user.first_name, 'shirt_size': str_shirt}),
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[obj_user.email])
        messages.info(request, "Email sent to %s." % obj_user.email)


shirt_reminder.short_description = "Send shirt size reminder"


class ShirtAdmin(admin.ModelAdmin):
    list_filter = ('event', 'shirt_size')
    list_display = ('event', 'fan', 'shirt_size', 'date_ordered')
    search_fields = ('fan__first_name', 'fan__last_name', 'date_ordered')
    actions = [shirt_ordered, shirt_reminder]


admin.site.register(Shirt, ShirtAdmin)
