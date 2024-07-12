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