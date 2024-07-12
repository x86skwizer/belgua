from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
	path('index.html', views.index, name='index'),
	path('', views.index, name='index'),
	path('contact.html', views.contact, name='contact'),
	path('contact/', views.contact, name='contact'),
	path('contact', views.contact, name='contact'),
	path('cart.html', views.cart, name='cart'),
	path('cart/', views.cart, name='cart'),
	path('cart', views.cart, name='cart'),
	path('product-list.html', views.product_list, name='product-list'),
	path('product-list/', views.product_list, name='product-list'),
	path('product-list', views.product_list, name='product-list'),
	path('product-detail.html', views.product_detail, name='product-detail'),
	path('product-detail/', views.product_detail, name='product-detail'),
	path('product-detail', views.product_detail, name='product-detail'),
	path('checkout.html', views.checkout, name='checkout'),
	path('checkout/', views.checkout, name='checkout'),
	path('checkout', views.checkout, name='checkout'),
]