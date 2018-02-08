from django.contrib import admin
from .models import Business, Vendor, Sponsor
# Register your models here.

admin.site.register(Vendor)
admin.site.register(Sponsor)
admin.site.register(Business)
