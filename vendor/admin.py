from django.contrib import admin
from .models import Business, BusinessNote, Vendor, Sponsor
# Register your models here.


class BusinessNoteAdmin(admin.TabularInline):
    model = BusinessNote
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class BusinessAdmin(admin.ModelAdmin):
    ordering = ('name', 'locality', 'region')
    list_filter = ('locality', 'region')
    list_display = ('name', 'phone_number', 'street',
                    'locality', 'region', 'country', 'url')
    list_display_links = ('name',)
    inlines = [BusinessNoteAdmin]


class SponsorAdmin(admin.ModelAdmin):
    ordering = ('event', 'business', 'status')
    list_filter = ('event', 'status')
    list_display = ('event', 'user', 'business', 'product',
                    'product_quantity', 'status')
    list_display_links = ('business',)


class VendorAdmin(admin.ModelAdmin):
    ordering = ('event', 'business', 'status')
    list_filter = ('event', 'status')
    list_display = ('event', 'user', 'business', 'product',
                    'product_quantity', 'status')
    list_display_links = ('business',)


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Business, BusinessAdmin)
