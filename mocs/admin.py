from django.contrib import admin

from .models import Category, EventCategory, MocCategories, MocNote, Moc, Vote, PublicVote


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


class MocNoteInLine(admin.TabularInline):
    model = MocNote
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MOCCategoryInLine(admin.TabularInline):
    model = MocCategories
    extra = 1


class MOCAdmin(admin.ModelAdmin):
    # List display for the admin
    inlines = (MOCCategoryInLine, MocNoteInLine)
    list_display_links = ('title', )
    list_display = ('creator', 'title', 'year_built',
                    'year_retired', 'is_public')
    search_fields = ('title', 'description',
                     'creator__last_name', 'creator__first_name')


admin.site.register(Moc, MOCAdmin)


class PublicVoteAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('session', 'moc', 'category',)


admin.site.register(PublicVote, PublicVoteAdmin)


class VoteAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('fan', 'moc', 'category', 'value')


admin.site.register(Vote, VoteAdmin)
