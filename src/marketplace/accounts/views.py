from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CompanyRegistrationForm, FreelancerRegistrationForm



from django.http import HttpResponse

from .forms import LoginForm, UserRegistrationForm

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username = cd['username'],
                                password = cd['password']) # None
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Usuario autenticado')
                else:
                    return HttpResponse('El usuario no esta activo')
            else:
                return HttpResponse('La información no es correcta')
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    
@login_required

def dashboard(request):
    return render(request, 'accounts/dashboard.html') 


# Registro de una empresa
def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            new_company = form.save(commit=False)
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            new_company.user = user
            new_company.save()
            return redirect('registration_success')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'accounts/register_company.html', {'form': form})

# Registro de un freelancer
def register_freelancer(request):
    if request.method == 'POST':
        form = FreelancerRegistrationForm(request.POST)
        if form.is_valid():
            new_freelancer = form.save(commit=False)
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            new_freelancer.user = user
            new_freelancer.save()
            return redirect('registration_success')
    else:
        form = FreelancerRegistrationForm()
    return render(request, 'accounts/register_freelancer.html', {'form': form})

from django.shortcuts import render

def register(request):
    return render(request, 'accounts/register.html')


def registration_success(request):
    return render(request, 'accounts/registration_success.html')