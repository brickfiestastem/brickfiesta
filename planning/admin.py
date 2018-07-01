from django.contrib import admin

from .models import Program, ProgramContributors, ProgramHighlightActivity, BagCheckListItems


class ProgramContributorsInLine(admin.TabularInline):
    model = ProgramContributors
    extra = 0


class ProgramHighlightActivityInLine(admin.TabularInline):
    model = ProgramHighlightActivity
    extra = 0


class ProgramAdmin(admin.ModelAdmin):
    # List display for the admin

    inlines = (ProgramContributorsInLine, ProgramHighlightActivityInLine)
    list_filter = ('event', )
    list_display = ('event', )

admin.site.register(Program, ProgramAdmin)


class BagCheckListAdmin(admin.ModelAdmin):
    list_display_links = ('item',)
    list_display = ('product', 'item', )

admin.site.register(BagCheckListItems, BagCheckListAdmin)