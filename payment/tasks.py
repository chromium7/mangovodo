from io import BytesIO
from celery import task
import weasyprint

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from orders.models import Order


@task
def payment_completed(order_id):
    '''
    Task to send an email notification when payment is successful
    '''
    order = Order.objects.get(id=order_id)

    subject = f'Mangovodo - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase'
    email = EmailMessage(
        subject, message, 'admin@example.com', [order.buyer.email])

    # Generate invoice PDF
    html = render_to_string('order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]

    weasyprint.HTML(string=html).write_pdf(stylesheets=stylesheets)

    # Attach PDF to email
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    # Send email
    email.send()
