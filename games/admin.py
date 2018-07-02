from django.contrib import admin

from .models import DoorPrizeWinner, DoorPrizePool


class DoorPrizePoolAdmin(admin.ModelAdmin):
    # List display for the admin
    ordering = ('created',)
    list_display = ('schedule', 'fan', 'created')
    list_display_links = ('fan',)


admin.site.register(DoorPrizePool, DoorPrizePoolAdmin)


class DoorPrizeWinnerAdmin(admin.ModelAdmin):
    # List display for the admin
    ordering = ('created',)
    list_display = ('event', 'fan', 'created')
    list_display_links = ('fan',)


admin.site.register(DoorPrizeWinner, DoorPrizeWinnerAdmin)
