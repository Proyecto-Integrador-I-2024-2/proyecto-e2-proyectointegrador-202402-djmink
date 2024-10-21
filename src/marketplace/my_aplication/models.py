from django.db import models
from django.utils import timezone
from perfil.models import Project

class Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    class Meta:
        abstract = True

class FreelancerProfile(Profile):
    pass 

class Skill(models.Model):
    name = models.CharField(max_length=100)
    freelancer_profile = models.ForeignKey(FreelancerProfile, on_delete=models.PROTECT, related_name='skills')

class Experience(models.Model):
    company_name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=1000)
    freelancer_profile = models.ForeignKey(FreelancerProfile, on_delete=models.PROTECT, related_name='experiences')

class Portfolio(models.Model):
    freelancer_profile = models.ForeignKey(FreelancerProfile, on_delete=models.PROTECT, related_name='portfolios')

class Content(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=300)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.PROTECT, related_name='contents')

class CompanyProfile(Profile):
    address = models.CharField(max_length=100)

class Rate(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=1)
    date = models.DateField(default=timezone.now)
    comment = models.CharField(max_length=200)
    profile = models.ForeignKey(FreelancerProfile, on_delete=models.PROTECT, related_name='rates')

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='users')

    class Meta:
        abstract = True

class CompanyManager(User):
    profile = models.ForeignKey(CompanyProfile, on_delete=models.PROTECT, related_name='company_managers')

class Freelancer(User):
    profile = models.ForeignKey(FreelancerProfile, on_delete=models.PROTECT, related_name='freelancers')

class Publication(models.Model):
    date = models.DateField()
    company_manager = models.ForeignKey(CompanyManager, on_delete=models.PROTECT, related_name='publications')

class Contract(models.Model):
    date = models.DateField()
    company_manager = models.ForeignKey(CompanyManager, on_delete=models.PROTECT, related_name='contracts')
    freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='contracts')

class Payment(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    company_manager = models.ForeignKey(CompanyManager, on_delete=models.PROTECT, related_name='payments')
    freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='payments')

class Requirement(models.Model):
    title = models.CharField(max_length=50, default='New Requirement')
    description = models.CharField(max_length=500, default='No description provided.')
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='requirements')

class Application(models.Model):
    date = models.DateField(auto_now_add=True)  # Automatically set to the current date when created
    freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='applications')
    accepted = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='applications')
    requirement = models.ForeignKey(Requirement, on_delete=models.PROTECT, related_name='applications')


class Reference(models.Model):
    position = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    experience = models.ForeignKey(Experience, on_delete=models.PROTECT, related_name='references')

class Chat(models.Model):
    pass