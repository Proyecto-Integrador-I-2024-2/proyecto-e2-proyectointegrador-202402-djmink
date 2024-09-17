from django.shortcuts import render, get_object_or_404
from .forms import RegisterForm, CompleteProfileForm

from django.shortcuts import render, redirect
from .models import FreelancerProfile, Freelancer, User
from .forms import RegisterForm

def users(request):
    users = Freelancer.objects.all()
    return render(request, 'my_aplication/users.html', {'users': users})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            freelancer_profile = FreelancerProfile.objects.create(
                name= "",
                email= "",
                phone= ""
            )

            freelancer = Freelancer.objects.create(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                profile=freelancer_profile 
            )
            
            return redirect('complete', profile_id=freelancer_profile.id)
    else:
        form = RegisterForm()

    return render(request, 'my_aplication/register.html', {'form': form})

def complete(request, profile_id):

    freelancer_profile = get_object_or_404(FreelancerProfile, id=profile_id)

    if request.method == 'POST':
        form = CompleteProfileForm(request.POST, instance=freelancer_profile)
        if form.is_valid():
            form.save()
            
            return redirect('users')
    else:
        form = CompleteProfileForm(instance=freelancer_profile)

    return render(request, 'my_aplication/complete_profile.html', {'form': form})