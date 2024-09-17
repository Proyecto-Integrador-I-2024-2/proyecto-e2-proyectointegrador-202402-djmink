from django import forms
from .models import Freelancer, FreelancerProfile

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ['username', 'password']

class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = ['name', 'email', 'phone']