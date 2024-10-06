from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CompanyRegistrationForm, FreelancerRegistrationForm, LoginForm
from django.contrib.auth.views import LoginView

# accounts/views.py
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Asegúrate de que esta sea la ruta correcta a tu plantilla de login
    redirect_authenticated_user = True    # Si ya está autenticado, redirigir a la página principal
    