from .cart import Cart
from .forms import CartAddProductForm


def cart(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True,
        })
    return {'cart': cart, 'cart_form': CartAddProductForm()}
