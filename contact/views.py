from django.shortcuts import render,redirect
from .models import ContactData
from django.contrib import messages
# Create your views here.

def contact_message(request, *args, **kwargs):
    print(request.method)
    if request.method == 'POST':
        name = request.POST['name']
        print(name)
        email = request.POST['email']
        print(email)
        phone_no = request.POST['phone_no']
        text_data = request.POST['text_data']

        ContactData.objects.create(name = name, email = email, phone_no = phone_no, text = text_data)
        messages.success(request, "Message sent successfully")
        return redirect("contact-page")
    else:
        print("no data entered")
        
    return render(request, 'contact_page/index.html')
