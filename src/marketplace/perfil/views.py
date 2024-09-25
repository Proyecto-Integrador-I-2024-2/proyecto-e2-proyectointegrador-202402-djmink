from django.http import Http404
from django.shortcuts import render, get_object_or_404
from my_aplication.models import Profile, FreelancerProfile, CompanyProfile
 # get the current user model

# Create your views here.
def perfilesFreelancer(request, freelancer_profile_id):
    profile = get_object_or_404(FreelancerProfile, pk=freelancer_profile_id)
    return render(request, 'perfil/perfil_freelancer.html', {'profile': profile})
    
        
def perfilesCliente(request, company_profile_id):        
    profile = get_object_or_404(CompanyProfile, pk=company_profile_id)
    return render(request, 'perfil/perfil_cliente.html', {'profile': profile})


