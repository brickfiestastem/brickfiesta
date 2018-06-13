from django.contrib import admin
from .models import Category, EventCategory, MocCategories, Moc, Vote


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


class MOCCategoryInLine(admin.TabularInline):
    model = MocCategories
    extra = 1


class MOCAdmin(admin.ModelAdmin):
    # List display for the admin
    inlines = (MOCCategoryInLine, )
    list_display_links = ('title', )
    list_display = ('creator', 'title', 'year_built',
                    'year_retired', 'is_public')
    search_fields = ('title', 'description',
                     'creator__last_name', 'creator__first_name')


admin.site.register(Moc, MOCAdmin)


class VoteAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('fan', 'moc', 'category', 'value')


admin.site.register(Vote, VoteAdmin)
