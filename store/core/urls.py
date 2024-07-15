from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
	path('', views.index, name='index'),
	path('index/', views.index, name='index'),
	path('contact/', views.contact, name='contact'),
	path('cart/', views.cart, name='cart'),
	path('product-list/', views.product_list, name='product-list'),
	path('product-detail/<int:pk>', views.product_detail, name='product-detail'),
	path('checkout/', views.checkout, name='checkout'),
	path('my-account/', views.my_account, name='my-account'),
	path('wishlist/', views.wishlist, name='wishlist'),
	path('login/', views.login_user, name='login'),
	path('logout/', views.logout_user, name='logout'),
	path('register/', views.register_user, name='register'),
]