from django.contrib import admin
from .models import Category, EventCategory, Moc
# Register your models here.
admin.site.register(Category)
admin.site.register(EventCategory)
admin.site.register(Moc)
