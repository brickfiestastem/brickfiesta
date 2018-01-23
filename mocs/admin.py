from django.contrib import admin
from .models import Category, EventCategory, Moc, Vote

# Register your models here.
admin.site.register(Category)
admin.site.register(EventCategory)
admin.site.register(Moc)


class VoteAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('user', 'moc', 'category', 'value')


admin.site.register(Vote, VoteAdmin)
