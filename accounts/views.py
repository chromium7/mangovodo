from django.shortcuts import render, reverse, redirect
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied

from shop.forms import AddressRegistrationForm
from shop.models import Address
from orders.models import Order


def user_profile(request):
    user = request.user
    user_addresses = user.addresses.all()
    address_form = AddressRegistrationForm()
    purchases_paid = user.orders.filter(paid=True)
    purchases_pending = user.orders.filter(paid=False)

    return render(request, 'accounts/profile.html', {
        'addresses': user_addresses,
        'purchases_paid': purchases_paid,
        'purchases_pending': purchases_pending,
        'address_form': address_form,

    })


@require_POST
def add_address(request):
    form = AddressRegistrationForm(request.POST)
    if form.is_valid():
        user_address = form.save(commit=False)
        user_address.user = request.user
        user_address.save()

        return redirect(reverse('accounts:user_profile'))


def delete_address(request, address_id):
    address = Address.objects.get(id=address_id)
    # Check if the current user is owner of the address
    if address.user == request.user:
        address.delete()
        return redirect(reverse('accounts:user_profile'))
    else:
        raise PermissionDenied()


def pay_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.user == order.buyer:
        request.session['order_id'] = order_id
        return redirect(reverse('payment:process'))
    else:
        raise PermissionDenied()


def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.user == order.buyer:
        order.delete()
        return redirect(reverse('accounts:user_profile'))
    else:
        raise PermissionDenied()
