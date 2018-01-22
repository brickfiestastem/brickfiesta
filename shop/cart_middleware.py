from shop.models import Cart
import uuid


class InitializeCart:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.request_logic(request)
        response = self.get_response(request)
        self.response_logic()
        return response

    def request_logic(self, request):
        if not request.session.get('id', None):
            request.session['id'] = str(uuid.uuid4())
        # import ipdb; ipdb.set_trace()
        session = request.session.get('id')
        cart = Cart.objects.filter(session=session)
        if not cart:
            if not request.user.id:
                cart = Cart.objects.create(session=session)
            else:
                try:
                    cart = Cart.objects.get(user=request.user)
                    cart.session = session
                    cart.save()
                except Exception:
                    cart = Cart.objects.create(
                        session=session, user=request.user)
        else:
            cart = cart.first()
            if not cart.user and request.user.id:
                cart.user = request.user
                cart.save()
        request.session['cart'] = str(cart.id)

    def response_logic(self):
        pass
