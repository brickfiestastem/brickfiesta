from django.contrib import admin
from .models import Product, ProductType, Order, OrderItem, Cart, CartItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'product_type', 'price')

admin.site.register(Product, ProductAdmin)

class ProductTypeAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('title', 'created')

admin.site.register(ProductType, ProductTypeAdmin)

class OrderAdmin(admin.ModelAdmin):
    # List display for the admin
    list_display = ('id','user', 'created')

admin.site.register(Order, OrderAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('session',)

admin.site.register(Cart, CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'first_name', 'last_name', 'email', 'product')

admin.site.register(CartItem, CartItemAdmin)
