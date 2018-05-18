from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Attendee, Badge, Profile, Shirt
from django.core.mail import send_mail
import uuid


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


def fix_order_password(modeladmin, request, queryset):
    for obj_user in queryset:
        obj_user.set_password(uuid.uuid4())
        obj_user.save()
        send_mail(subject="Brick Fiesta - New Account Created",
                  message="Yourself or someone you know has purchased a product from Brick Fiesta that "
                          "requires an account. We have created an account for you and set a random "
                          "password. You will need to go to "
                          "https://www.brickfiesta.com/afol/password_reset/"
                          " and enter the email that received this message to start the password reset "
                          "process."
                          " Once the password is reset you will be able to log in and have access to"
                          " all the different options the product enabled in your account.",
                  from_email='customer.support@gmail.com',
                  recipient_list=[obj_user.email])


fix_order_password.short_description = "Fix users order password problem"


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
    list_display = ('event', 'user', 'shirt_size')


admin.site.register(Shirt, ShirtAdmin)
