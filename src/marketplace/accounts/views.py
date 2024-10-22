from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CompanyRegistrationForm, FreelancerRegistrationForm, LoginForm
from django.contrib.auth.views import LoginView


from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'  
    redirect_authenticated_user = True   
    
