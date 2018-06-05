from django.contrib import admin
from .models import Product, Order, OrderItem, CartItem, ProductBulletPoint
from django.contrib import messages
from .utils import add_attendee_fan_badge_shirt


class ProductBulletPointInline(admin.TabularInline):
    model = ProductBulletPoint
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductBulletPointInline,)
    list_filter = ('event', 'product_type', 'is_public')
    list_display = ('title', 'event', 'product_type', 'is_public', 'price')


admin.site.register(Product, ProductAdmin)


class OrderItemInLine(admin.TabularInline):
    model = OrderItem


def reprocess_order(modeladmin, request, queryset):
    for obj_order in queryset:
        for obj_item in OrderItem.objects.filter(order=obj_order):
            add_attendee_fan_badge_shirt(request, obj_item)
            messages.info(request, "Added fan and attendee for {}.".format(str(obj_item)))


reprocess_order.short_description = "Reprocess order items for fan and attendee linkage"


class OrderAdmin(admin.ModelAdmin):
    # List display for the admin
    inlines = (OrderItemInLine, )
    list_display = ('id', 'user', 'created')
    actions = [reprocess_order]


admin.site.register(Order, OrderAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_filter = ('product__event', 'product__product_type')
    list_display = ('cart', 'first_name', 'last_name', 'email', 'product')


admin.site.register(CartItem, CartItemAdmin)
