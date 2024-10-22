from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CompanyRegistrationForm, FreelancerRegistrationForm, LoginForm
from django.contrib.auth.views import LoginView

#SMTP libraries
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from marketplace.settings import EMAIL_HOST_USER

class CustomLoginView(LoginView):
    template_name = 'login.html'  
    redirect_authenticated_user = True   
    
def register(request):
    return render(request, 'register.html')

def recover(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        #enviar mensaje por correo usando SMTP y el email
        send_recovery_email(email, 'prueba123')

        return redirect('recover_confirmation')
    else:
        return render(request, 'PasswordRecovery.html')

def recover_confirmation(request):
    return render(request, 'PasswordRecoveryConfirmation.html')

def send_recovery_email(email, password):
    message = "Dear user, in response to your request, we are sending you your password: " + password
    send_mail('Recover your password!',message,EMAIL_HOST_USER,[email],fail_silently=False)