from django.shortcuts import render, get_object_or_404
from my_aplication.models import User, FreelancerProfile, CompanyProfile

# Create your views here.
def perfil(request, user_id):
    user = User.objects.get(id=user_id) 
    # get_object_or_404(User, id=user_id)
    if user.is_freelancer:
        profile = FreelancerProfile.objects.get(user=user)
        return render(request, 'perfil/perfil_freelancer.html', {'profile': profile})
    else:
        profile = CompanyProfile.objects.get(user=user)
        return render(request, 'perfil/perfil_cliente.html', {'profile': profile})

