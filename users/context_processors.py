from products.models import Cart

def carts(request):
    user = request.user
    cart = Cart.objects.filter(user=user) if user.is_authenticated else []
    return {'carts': cart}
