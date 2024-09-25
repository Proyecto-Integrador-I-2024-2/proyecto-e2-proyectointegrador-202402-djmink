from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Usuario autenticado')  # Aquí corregimos el uso de HttpResponse
                else:
                    return HttpResponse('El usuario no está activo')  # También corregido
            else:
                return HttpResponse('La información no es correcta')  # También corregido
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
