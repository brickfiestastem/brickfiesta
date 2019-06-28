from django.contrib import admin
from .models import Donations, DonationNotes


# Register your models here.


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
    inlines = [DonationNotesAdmin]
    search_fields = ['item', 'item_value', 'fan', 'business']


admin.site.register(Donations, DonationsAdmin)
