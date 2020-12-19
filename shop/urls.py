from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('<slug:category_slug>/', views.listing, name='listing'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
 
]
