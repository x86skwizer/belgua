from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserFrom, ChangePasswordForm, UserInfoForm
from django import forms
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.contrib import messages
from .models import Product, Category, Profile
from django.db.models import Q
import random, json
from cart.cart import Cart

# Create your views here
def index(request):
	products = list(Product.objects.all())
	random.shuffle(products)
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

def category_summary(request):
		categories = Category.objects.all()
		return render(request, 'category_summary.html', {"categories": categories})

def category(request, foo):
	# Replace Hyphens with spaces
	foo = foo.replace('-', ' ')
	# Grab category from URL
	try:
		# Look Up category
		category = Category.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products': products, 'category': category})
	except:
		messages.success(request, ("Category doesn't exist !"))
		return redirect('core:index')

def product_detail(request, pk):
	products = list(Product.objects.all())
	product = Product.objects.get(id=pk)
	random.shuffle(products)
	return render(request, 'product-detail.html', {'products': products, 'product': product})

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserFrom(request.POST or None, instance=current_user)
		if user_form.is_valid():
			user_form.save()
			login(request, current_user)
			messages.success(request, "User has been updated !")
			return redirect('core:index')
		return render(request, 'my-account.html', {'user_form': user_form})
	else:
		messages.success(request, "Something went wrong !")
		return redirect('core:update_user')

def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		if request.method == "POST":
			form = ChangePasswordForm(current_user, request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, "Password has been changed !")
				return redirect('core:login')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('core:update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form': form})
	else:
		messages.success(request, "Something went wrong !")
		return redirect('core:index')

def update_info(request):
    if request.user.is_authenticated:
        # Get Current User
        current_user = get_object_or_404(Profile, user__id=request.user.id)
        
        # Get current user shipping info
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            shipping_user = None
        
        # Get Original user form
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        # Get user shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Info has been updated!")
            return redirect('core:index')
        
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.error(request, "You need to be logged in to update your information.")
        return redirect('core:index')

def search(request):
	# Determine if they filled out
	products = list(Product.objects.all())
	random.shuffle(products)
	if request.method == "POST":
		searched = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		# Test for null
		if not searched:
			messages.success(request, ("Product not found ... Try again !"))
			return render(request, "search.html", {'products':products})
		return render(request, "search.html", {'searched':searched, 'products':products})
	else:
		return render(request, "search.html", {'products':products})

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			# Old Cart Logic
			current_user = Profile.objects.get(user__id=request.user.id)
			# Get their saved cart from database
			saved_cart = current_user.old_cart
			# Convert database string to python dictionary
			if saved_cart:
				# Convert to dictionnary using JSON
				converted_cart = json.loads(saved_cart)
				# Add the loaded cart dictionary to our session
				# Get the cart
				cart = Cart(request)
				# Loop through the cart and add the items from the dictionary
				for key, value in converted_cart.items():
					cart.db_add(product=key, quantity=value)

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
			messages.success(request, ("You have registered successfully ! - (Please fill out your user info)"))
			return redirect('core:update_info')
		else:
			messages.success(request, ("Your registeriation has failed !"))
			return redirect('core:register')

	else:
		return render(request, 'register.html', {'form': form})