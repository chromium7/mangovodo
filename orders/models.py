from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from shop.models import Product, Address
from coupons.models import Coupon


class Order(models.Model):
    buyer = models.ForeignKey(
        User, related_name='orders', on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, related_name='orders', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(
        Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"Order {self.id}"

    def total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - self.get_discount()

    def get_discount(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost*(self.discount / Decimal(100))


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
