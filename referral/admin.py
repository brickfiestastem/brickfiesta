from django.contrib import admin

# Register your models here.

from .models import Referral


class ReferralAdmin(admin.ModelAdmin):
    ordering = ("event__start_date",)
    list_filter = ("event",)
    list_display_links = ('group_name',)
    list_display = ('event', 'group_name', 'code', 'url', 'count')


admin.site.register(Referral, ReferralAdmin)
