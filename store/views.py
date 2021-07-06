from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
import datetime
from .utils import CookieCart, CartData
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def store(request):
    context = {'products': Product.objects.all()}
    return render(request, 'store/store.html', context)


def registration(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            # messages.success(request, 'Account was successfully created' + user)
            return redirect('log_in')

    context = {'form': form}

    return render(request, 'store/registration.html', context)


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Username or password are incorrect')
            return render(request, 'store/log_in.html')

    return render(request, 'store/log_in.html')


@login_required(login_url='log_in')
def log_out(request):
    logout(request)
    return redirect('log_in')


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
