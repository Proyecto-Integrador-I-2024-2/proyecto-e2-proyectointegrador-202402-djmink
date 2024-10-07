from django.http import Http404
from django.shortcuts import render, get_object_or_404
from perfil.models import Profile, ClientProfile, Publication, ProjectCategory, SocialNetwork
 # get the current user model

# Create your views here.
def perfilesFreelancer(request, id):
    
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/perfil_freelancer.html', {'p': p})

def mainFreelancer(request, id):        
    profile = get_object_or_404(Profile, id=id)
    publications = Publication.objects.all()
    categories = ProjectCategory.objects.all()
    companies = ClientProfile.objects.filter(projects__publications__isnull=False).distinct()
    return render(request, 'perfil/main_freelancer.html', {'profile': profile, 'publications':publications, 'categories': categories, 'companies':companies})

def editAccount(request, id):
    p = get_object_or_404(Profile, id=id)

    # Se debe cambiar
    if '-' in p.phone:
        code = p.phone.split('-')[0]
        phone = p.phone.split('-')[1]
    else:
        code = p.phone
        phone = p.phone

    return render(request, 'perfil/edit_profile_account.html', {'p': p, 'code': code, 'phone': phone})

def editProfile(request, id=id):
    p = get_object_or_404(Profile, id=id)
    existing_types = p.social_networks.values_list('type', flat=True)
    available_media = [choice for choice in SocialNetwork.TYPE_CHOICES if choice[0] not in existing_types]

    return render(request, 'perfil/edit_profile.html', {'p': p, 'available_media': available_media})

def deleteDisable(request, id=id):
    p = get_object_or_404(Profile, id=id)
    return render(request, 'perfil/edit_profile_delete.html', {'p': p})

#def editar_perfil_sessions(request, id=id):
#    p = get_object_or_404(Profile, id=id)
#    return render(request, 'perfil/edit_profile4.html', {'p': p})
        
def perfilesCliente(request, id):        
    p = get_object_or_404(ClientProfile, id=id)
    return render(request, 'perfil/perfil_cliente.html', {'p':p})

def mainCliente(request, id):        
    p = get_object_or_404(ClientProfile, id=id)
    return render(request, 'perfil/main_client.html', {'p':p})
