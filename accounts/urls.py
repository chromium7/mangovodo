from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('user/', views.user_profile, name='user_profile'),
    path('add_address/', views.add_address, name='add_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('pay_order/<int:order_id>/', views.pay_order, name='pay_order'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    
]
