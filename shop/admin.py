from django.contrib import admin
from .models import Product, Order, OrderItem, CartItem, ProductBulletPoint
from afol.models import Attendee, Fan
from django.contrib import messages


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
            obj_fan, is_created = Fan.objects.get_or_create(user=obj_item.user,
                                                            first_name=obj_item.first_name,
                                                            last_name=obj_item.last_name)

            obj_attendee = None
            if is_created:
                obj_fan.save()

            if obj_item.product.product_type == 'vendor':
                obj_attendee, is_created = Attendee.objects.get_or_create(event=obj_item.product.event,
                                                                          fan=obj_fan,
                                                                          role='vendor')
                if is_created:
                    obj_attendee.save()
            if obj_item.product.product_type == 'sponsor':
                obj_attendee, is_created = Attendee.objects.get_or_create(event=obj_item.product.event,
                                                                          fan=obj_fan,
                                                                          role='sponsor')
                if is_created:
                    obj_attendee.save()
            if obj_item.product.product_type == 'convention':
                obj_attendee, is_created = Attendee.objects.get_or_create(event=obj_item.product.event,
                                                                          fan=obj_fan,
                                                                          role='attendee')
                if is_created:
                    obj_attendee.save()
            messages.info(request, "Added fan {} and attendee {}.".format(
                str(obj_fan), str(obj_attendee)))


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
