from django import forms
from django.contrib.auth.models import User
from my_aplication.models import CompanyManager, Freelancer

#class LoginForm(forms.Form):
#    username = forms.CharField(label='Username', max_length=150, required=True)
#    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)

#class CompanyRegistrationForm(forms.ModelForm):
#   class Meta:
#        model = CompanyManager
#        fields = ['name', 'legal_agent', 'phone']
#        labels = {
#            'name': 'Company Name',
#            'legal_agent': 'Legal Agent',
#            'phone': 'Phone Number',
#        }
#        help_texts = {
#            'phone': 'Please enter a valid phone number.',
#        }

#class FreelancerRegistrationForm(forms.ModelForm):
#    class Meta:
#        model = Freelancer
#        fields = ['name', 'portfolio_url', 'skills', 'phone']
#        labels = {
#            'name': 'Full Name',
#            'portfolio_url': 'Portfolio URL',
#            'skills': 'Skills',
#            'phone': 'Phone Number',
#        }
#        help_texts = {
#            'portfolio_url': 'Enter the URL to your portfolio.',
#            'phone': 'Please enter a valid phone number.',
#        }
#class UserRegistrationForm(forms.ModelForm):
#    password = forms.CharField(widget=forms.PasswordInput)

#    class Meta:
#        model = User
#        fields = ['username', 'email', 'password']