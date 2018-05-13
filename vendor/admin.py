from django.contrib import admin
from .models import Business, BusinessNote, Vendor, Sponsor
from django.core.management import call_command
from django.conf import settings
import os
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


class SponsorAdmin(admin.ModelAdmin):
    ordering = ('event', 'business', 'status')
    list_filter = ('event', 'status')
    list_display = ('event', 'user', 'business', 'product',
                    'product_quantity', 'status', 'created')
    list_display_links = ('business',)


class VendorAdmin(admin.ModelAdmin):
    ordering = ('event', 'business', 'status')
    list_filter = ('event', 'status')
    list_display = ('event', 'user', 'business', 'product',
                    'product_quantity', 'status', 'created')
    list_display_links = ('business',)


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Business, BusinessAdmin)
