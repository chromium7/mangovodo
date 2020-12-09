import weasyprint

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required

from cart.cart import Cart
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender

from .models import Order, OrderItem
from .forms import OrderCreateForm
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    coupon_form = CouponApplyForm()
    if request.method == 'POST':
        form = OrderCreateForm(user=request.user, data=request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.buyer = request.user
            order.save()

            # Add into Recommender
            r = Recommender()
            r.products_bought([item['product'] for item in cart])

            # Cart
            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()

            # Launch asynchronous task
            order_created.delay(order.id)

            request.session['order_id'] = order.id

            return redirect(reverse('payment:process'))

            # return render(request, 'order/created.html', {
            #     'order': order,
            # })
    else:
        form = OrderCreateForm(user=request.user)

    return render(request, 'order/create.html', {
        'cart': cart,
        'form': form,
        'coupon_form': coupon_form,
    })


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order_id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
        weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {
        'order': order,
    })
