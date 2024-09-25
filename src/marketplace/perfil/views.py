from django.http import Http404
from django.shortcuts import render, get_object_or_404
from my_aplication.models import User, Freelancer, FreelancerProfile, CompanyProfile, CompanyManager
from django.contrib.auth import get_user_model

User = get_user_model()  # get the current user model

# Create your views here.
def perfil(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if isinstance(user, Freelancer):
        profile = FreelancerProfile.objects.get(user=user)
        return render(request, 'perfil/perfil_freelancer.html', {'profile': profile})
    elif isinstance(user, CompanyManager):
        profile = CompanyProfile.objects.get(user=user)
        return render(request, 'perfil/perfil_cliente.html', {'profile': profile})
    else: 
        raise Http404('Perfil no encontrado')
    
def perfiles(request):
    return render(request, 'perfil/perfiles.html')

