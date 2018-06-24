import os
import uuid

from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.core.mail import send_mail
from django.core.management import call_command
from django.template import loader

from shop.models import CartItem
from .models import Business, BusinessNote, Vendor, Sponsor


# Register your models here.


class BusinessNoteAdmin(admin.TabularInline):
    model = BusinessNote
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


def adjust_logo(modeladmin, request, queryset):
    for obj_business in queryset:
        messages.info(request, "Attempting to adjust {}.".format(
            obj_business.logo.url))
        call_command('square_image', os.path.join(
            settings.MEDIA_ROOT, str(obj_business.logo)))


adjust_logo.short_description = "Adjust the business logo to be square"


class BusinessAdmin(admin.ModelAdmin):
    ordering = ('name', 'locality', 'region')
    list_filter = ('locality', 'region')
    list_display = ('name', 'phone_number', 'street',
                    'locality', 'region', 'country', 'url')
    list_display_links = ('name',)
    inlines = [BusinessNoteAdmin]
    actions = [adjust_logo]
    search_fields = ['name', 'phone_number', 'street', 'url']


admin.site.register(Business, BusinessAdmin)


def send_payment_reminder(modeladmin, request, queryset):
    for obj_vendor in queryset:
        obj_vendor.status = 'pending'
        obj_vendor.save()

        str_uuid = uuid.uuid4()
        obj_user = obj_vendor.user
        int_quantity = obj_vendor.product_quantity
        for int_item in range(int_quantity):
            basket_item = CartItem.objects.create(cart=str_uuid,
                                                  first_name=obj_user.first_name,
                                                  last_name=obj_user.last_name,
                                                  email=obj_user.email,
                                                  product=obj_vendor.product)
            messages.info(request, "Added {} to {} cart.".format(
                obj_vendor.product, obj_user))
        send_mail(subject="Brick Fiesta - Business Cart Assist",
                  message=loader.render_to_string(
                      "vendor/business_payment_email.html",
                      {'user_first_name': obj_user.first_name, 'token': str_uuid}),
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[obj_user.email])
        messages.info(request, "Email sent to %s." % obj_user.email)


send_payment_reminder.short_description = "Update to payment pending and send shopping cart link"


class SponsorAdmin(admin.ModelAdmin):
    ordering = ('event', 'business', 'status')
    list_filter = ('event', 'status')
    list_display = ('event', 'user', 'business', 'product',
                    'product_quantity', 'status', 'created')
    list_display_links = ('business',)
    search_fields = ('user__first_name', 'user__last_name', 'business__name')
    actions = [send_payment_reminder]


admin.site.register(Sponsor, SponsorAdmin)


class VendorAdmin(admin.ModelAdmin):
    ordering = ('event', 'business', 'status')
    list_filter = ('event', 'status')
    list_display = ('event', 'user', 'business', 'product',
                    'product_quantity', 'status', 'created')
    list_display_links = ('business',)
    search_fields = ('user__first_name', 'user__last_name', 'business__name')
    actions = [send_payment_reminder]


admin.site.register(Vendor, VendorAdmin)
