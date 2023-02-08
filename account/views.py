from django.shortcuts import render, redirect
from .models import Account
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
#from django.conf import settings
from .tokens import account_activation_token
# Create your views here.


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
        return redirect


# Activate account
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('login')

# Send accout to email to activate
def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("auth/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    #email = EmailMessage(mail_subject, settings.EMAIL_FROM, message, to=[to_email])
    
    #email.send(fail_silently=False)
    messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    

def register(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = Account.objects.create(first_name = firstname, last_name = lastname, username = username, email = email)
        user.is_active = False
        user.set_password(password)
        user.save()
        activateEmail(request, user, email)
        destination = kwargs.get("next")
        if destination:
            return redirect(destination)
        return redirect("login")
    
    return render(request, 'auth/register_page.html')

def login_page(request):
    if request.user.is_authenticated:
        redirect('index')
    destination = get_redirect_if_exists(request)

    if request.method == 'POST':
        username =request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                if destination:
                    return redirect(destination)
                messages.success(request, "Login successful")
                
                return redirect('index')
            else:
                print("User not authenticated")
                messages.warning(request, "User not authenticated")
                print("User not authenticated")
                return redirect('login')
        else:
            messages.warning(request, "Invalid User")
            print("Invlid User")
            return redirect('login')
    return render(request, 'auth/login_page.html')

@login_required
def logout_page(request):
    logout(request)
    return redirect("index")


@login_required
def resetPassword(request):
    user = request.user
    if user.is_authenticated:
        email = request.POST.get('email')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        if user.check_password(old_password):
            user_id = Account.objects.get(id = user.id, email = email)
            user_id.set_password(new_password)
            user_id.save()
            messages.success(request, 'Password reset successfully')
            redirect("reset-password")
        else:
            messages.info(request, 'Password does not match old password')
            redirect("reset-password")
    else:
        messages.warning(request, "User is not authenticatedtan")
    return render(request, 'auth/reset_password.html')

def forgetPassword(request):
    pass
            
