from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse, HttpResponse
import datetime
from .utils import CookieCart, CartData


def store(request):
    context = {'products': Product.objects.all()}
    return render(request, 'store/store.html', context)


def cart(request):
    data = CartData(request)
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, }

    # context = {'items': items, 'order': order, 'carItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = CartData(request)
    # cartItems = cookieData['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, }
    # context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action, 'ID:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        print('User is not loged in')
        print('Cookies', request.COOKIES)
        name = data['form']['name']
        number = data['form']['number']

        coockieData = CookieCart(request)
        items = coockieData['items']

        order = Order.objects.create(
            number_client=number,
            name_client=name,
            transaction_id=transaction_id,
            complete=False
        )

        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
        order.complete = True
        order.price = total
    order.save()


    ShippingAdress.objects.create(
        # customer=customer,
        order=order,
        oblast=data['shipping']['oblast'],
        rayon=data['shipping']['rayon'],
        gorod=data['shipping']['gorod'],
        np_otd=data['shipping']['otdeleniye'],
    )

    return JsonResponse('Payment was completed', safe=False)
