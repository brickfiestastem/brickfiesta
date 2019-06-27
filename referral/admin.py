import uuid
from django.contrib import admin

# Register your models here.

from .models import Referral


def referral_url(obj):
    return "https://www.brickfiesta.com/referral/" + str(obj.code)


referral_url.short_description = 'Referral URL'
referral_url.empty_value_display = 'Error'


class ReferralAdmin(admin.ModelAdmin):
    ordering = ("event__start_date",)
    list_filter = ("event",)
    list_display_links = ('group_name',)
    list_display = ('event', 'group_name', referral_url, 'url', 'count')


admin.site.register(Referral, ReferralAdmin)
