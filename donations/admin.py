from django.contrib import admin
from .models import Cause, Donations, DonationCauses, DonationNotes


# Register your models here.

class CauseAdmin(admin.ModelAdmin):
    ordering = ('-event', 'title', 'organization')
    list_filter = ('event', 'organization')
    list_display = ('event', 'title', 'organization')
    list_display_links = ('title',)
    search_fields = ['title', 'organization']


admin.site.register(Cause, CauseAdmin)


class DonationCausesAdmin(admin.TabularInline):
    model = DonationCauses
    extra = 1


class DonationNotesAdmin(admin.TabularInline):
    model = DonationNotes
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DonationsAdmin(admin.ModelAdmin):
    ordering = ('-event', 'fan', 'business', 'item')
    list_filter = ('event',)
    list_display = ('event', 'item', 'item_value', 'fan', 'business')
    list_display_links = ('item',)
    inlines = [DonationCausesAdmin, DonationNotesAdmin]
    search_fields = ['item', 'item_value', 'fan', 'business']


admin.site.register(Donations, DonationsAdmin)
