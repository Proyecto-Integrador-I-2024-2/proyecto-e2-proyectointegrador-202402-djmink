from django import forms
from my_aplication.models import Project, Milestone,Task
from django.contrib.auth.models import User

class createProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['manager', 'name', 'type', 'duration', 'description', 'budget', 'deadline', 'project_picture', 'state']

class editProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'type', 'duration', 'description', 'budget', 'deadline', 'project_picture', 'state']

class createMilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['name', 'description', 'project']

# class createMilestoneForm(forms.ModelForm):
#     class Meta:
#         model = Milestone
#         fields = ['name', 'description', 'deadline', 'project']  

# class createTaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ['name', 'description', 'deadline', 'milestone']


# class LoginForm(forms.Form):
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