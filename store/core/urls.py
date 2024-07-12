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
]