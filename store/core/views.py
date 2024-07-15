from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.contrib import messages
from .models import Product

# Create your views here
def index(request):
	products = Product.objects.all()
	return render(request, 'index.html', {'products': products})

def contact(request):
	if request.method == 'POST':
		message_name = request.POST['message-name']
		message_email = request.POST['message-email']
		message_subject = request.POST['message-subject']
		message = request.POST['message']

		#send an email
		send_mail(
			message_name, # subject
			message, # message
			message_email, # from email
			['yassineamrire00@gmail.com'], # To email
		)

		return render(request, 'contact.html', {'message_name': message_name})
	else:
		return render(request, 'contact.html')
	
def cart(request):
	return render(request, 'cart.html')

def product_list(request):
	return render(request, 'product-list.html')

def product_detail(request, pk):
	product = Product.objects.get(id=pk)
	return render(request, 'product-detail.html', {'product': product})

def checkout(request):
	return render(request, 'checkout.html')

def my_account(request):
	return render(request, 'my-account.html')

def wishlist(request):
	return render(request, 'wishlist.html')

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You have been logged in !"))
			return redirect('core:index')
		else:
			messages.success(request, ("Incorrect username or password !"))
			return redirect('core:login')

	else:
		return render(request, 'login.html')

def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out !"))
	return redirect('core:index')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			#log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("You have registered successfully !"))
			return redirect('core:index')
		else:
			messages.success(request, ("Your registeriation has failed !"))
			return redirect('core:register')

	else:
		return render(request, 'register.html', {'form': form})