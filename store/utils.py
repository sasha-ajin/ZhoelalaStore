import json
from .models import *


def CookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)

    items = []
    order = {'get_cart_total': 0, 'get_cart_items_quantity': 0, 'shipping': False}
    cartItems = order['get_cart_items_quantity']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items_quantity'] += cart[i]['quantity']

            item = {
                'id': product.id,
                'product': {'id': product.id, 'name': product.name, 'price': product.price,
                            'image': product.image},
                'quantity': cart[i]['quantity'],
                'digital': product.digital, 'get_total': total,
            }
            items.append(item)
        except:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}


def CartData(request):
    if request.user.is_authenticated:
        customer_ = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer_, complete=False)
        items = order.orderitem_set.all()
    else:
        cookieData = CookieCart(request)
        # cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return { 'order': order, 'items': items}
