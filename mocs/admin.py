from django.contrib import admin
from .models import Category, EventCategory, EventMoc, Moc, Vote


class CategoryAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('title', 'age_limit_min', 'age_limit_max')


admin.site.register(Category, CategoryAdmin)


class EventCategoryAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display_links = ('category', )
    list_filter = ('event', 'category',)
    list_display = ('event', 'category',)


admin.site.register(EventCategory, EventCategoryAdmin)


class EventMocAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display_links = ('moc', )
    list_filter = ('category',)
    list_display = ('category', 'fan', 'moc')


admin.site.register(EventMoc, EventMocAdmin)


class MocAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display_links = ('title', )
    list_display = ('creator', 'title', 'year_built',
                    'year_retired', 'is_public')


admin.site.register(Moc, MocAdmin)


class VoteAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('fan', 'moc', 'category', 'value')


admin.site.register(Vote, VoteAdmin)
