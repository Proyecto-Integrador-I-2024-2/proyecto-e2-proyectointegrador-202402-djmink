from django.http import Http404
from django.shortcuts import render, get_object_or_404
from perfil.models import Profile, ClientProfile
 # get the current user model

# Create your views here.
def perfilesFreelancer(request, id):
    
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/perfil_freelancer.html', {'p': p})

def editar_perfil(request, id):
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/edit_profile.html', {'p': p})

def editar_perfil_general(request, id=id):
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/edit_profile2.html', {'p': p})

def editar_perfil_password(request, id=id):
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/edit_profile3.html', {'p': p})

def editar_perfil_sessions(request, id=id):
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/edit_profile4.html', {'p': p})
        
def perfilesCliente(request, id):        
    p = get_object_or_404(ClientProfile, id=id)
    return render(request, 'perfil/perfil_cliente.html', {'p':p})

