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

    def create_cart(self, user=None, session=None):
        return Cart.objects.create(user=user, session=session)

    def request_logic(self, request):
        if not request.session.get('id', None):
            request.session['id'] = str(uuid.uuid4())
        session = request.session.get('id')
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
            except Cart.DoesNotExist:
                try:
                    cart = Cart.objects.get(session=session)
                    cart.user = request.user
                    cart.save()
                except Cart.DoesNotExist:
                    cart = self.create_cart(user=request.user, session=session)
        else:
            try:
                cart = Cart.objects.get(session=session)
            except Cart.DoesNotExist:
                cart = self.create_cart(session=session)
        request.session['cart'] = str(cart.id)

    def response_logic(self):
        pass
