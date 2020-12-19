from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.filter
def total_purchases(user):
    return user.orders.count()
