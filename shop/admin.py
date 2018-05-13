from django.contrib import admin
from .models import Product, Order, OrderItem, CartItem, ProductBulletPoint


class ProductBulletPointInline(admin.TabularInline):
    model = ProductBulletPoint
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductBulletPointInline,)
    list_display = ('title', 'event', 'product_type', 'price')


admin.site.register(Product, ProductAdmin)


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    max_num = 1


class OrderAdmin(admin.ModelAdmin):
    # List display for the admin
    inlines = (OrderItemInLine, )
    list_display = ('id', 'user', 'created')


admin.site.register(Order, OrderAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'first_name', 'last_name', 'email', 'product')


admin.site.register(CartItem, CartItemAdmin)
