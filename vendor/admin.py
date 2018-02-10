from django.contrib import admin
from .models import Business, Vendor, Sponsor
# Register your models here.


class BusinessAdmin(admin.ModelAdmin):
    ordering = ('name', 'locality', 'region')
    list_filter = ('locality', 'region')
    list_display = ('user', 'name', 'phone_number', 'locality', 'url')
    list_display_links = ('user', 'name',)


class SponsorAdmin(admin.ModelAdmin):
    ordering = ('event', 'business', 'status')
    list_filter = ('event', 'status')
    list_display = ('event', 'business', 'status')
    list_display_links = ('business',)


class VendorAdmin(admin.ModelAdmin):
    ordering = ('event', 'business', 'status')
    list_filter = ('event', 'status')
    list_display = ('event', 'business', 'status')
    list_display_links = ('business',)


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Business, BusinessAdmin)
