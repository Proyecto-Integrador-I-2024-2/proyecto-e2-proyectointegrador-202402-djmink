from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Profile, ClientProfile
 # get the current user model

# Create your views here.
def perfilesFreelancer(request, id):
    
    p = get_object_or_404(Profile, id=1)
    return render(request, 'perfil/perfil_freelancer.html', {'p': p})
    
        
def perfilesCliente(request, id):        
    p = get_object_or_404(ClientProfile, id=1)
    return render(request, 'perfil/perfil_cliente.html', {'p':p})


