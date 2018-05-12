from django.contrib import admin
from .models import Business, Vendor, Sponsor
# Register your models here.


class BusinessAdmin(admin.ModelAdmin):
    ordering = ('name', 'locality', 'region')
    list_filter = ('locality', 'region')
    list_display = ('name', 'phone_number', 'street', 'locality', 'region', 'country', 'url')
    list_display_links = ('name',)


class SponsorAdmin(admin.ModelAdmin):
    ordering = ('event', 'business', 'status')
    list_filter = ('event', 'status')
    list_display = ('event', 'user', 'business', 'product', 'product_quantity', 'status')
    list_display_links = ('business',)


class VendorAdmin(admin.ModelAdmin):
    ordering = ('event', 'business', 'status')
    list_filter = ('event', 'status')
    list_display = ('event', 'user', 'business', 'product', 'product_quantity', 'status')
    list_display_links = ('business',)


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Business, BusinessAdmin)
