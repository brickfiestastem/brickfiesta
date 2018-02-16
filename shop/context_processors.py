from shop.models import CartItem


def cart_count(request):
    cart_id = request.session.get('cart')
    count = 0
    if cart_id:
        count = CartItem.objects.filter(cart=cart_id).count()
    return {'cart_count': count}
