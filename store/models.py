from django.db import models
from django.contrib.auth.models import User


class Sizes(models.Model):
    size = models.IntegerField()

    def __str__(self):
        return str(self.size)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True)
    image = models.ImageField(null=True, blank=True)
    size = models.ManyToManyField(Sizes)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    number_client = models.CharField(max_length=100, null=True)
    name_client = models.CharField(max_length=100, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True)
    price = models.DecimalField(null=True,max_digits=10,decimal_places=2)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def shipping(self):
        shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items_quantity(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return str(self.pk)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.order.id)


class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    oblast = models.CharField(max_length=50, null=True)
    rayon = models.CharField(max_length=50, null=True)
    gorod = models.CharField(max_length=50, null=True)
    np_otd = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.order)
