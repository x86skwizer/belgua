from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.
def index(request):
	return render(request, 'index.html')

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

def product_detail(request):
	return render(request, 'product-detail.html')

def checkout(request):
	return render(request, 'checkout.html')

def my_account(request):
	return render(request, 'my-account.html')

def wishlist(request):
	return render(request, 'wishlist.html')

def login(request):
	return render(request, 'login.html')