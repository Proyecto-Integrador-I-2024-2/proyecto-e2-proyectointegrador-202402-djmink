'''
from django.db import models
from django.utils import timezone

class Profile(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

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
    legal_agent = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    business_vertical = models.CharField(max_length=100, null=True, blank=True)
    company_type = models.CharField(max_length=100, null=True, blank=True)

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
    identification = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)

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

class Application(models.Model):
    date = models.DateField()
    freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='applications')

class Reference(models.Model):
    position = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    experience = models.ForeignKey(Experience, on_delete=models.PROTECT, related_name='references')

class Chat(models.Model):
    pass
'''

## ------------------------------------------------------------
# Nueva adecuación del modelo
# Clases agrupadas, corregir a clases ya existentes en MER y MR

from django.db import models
from django.utils import timezone

class User(models.Model):
    # Datos básicos del usuario
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    
    # Datos del perfil común para Freelancers y Companies
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    

    # Datos compartidos de Freelancers y Companies
    date_joined = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.username} ({'Admin' if self.is_admin else 'User'})"

class Freelancer(User):
    # Datos específicos para Freelancer
    portfolio_url = models.URLField(max_length=255, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    identification = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)


class CompanyManager(User):
    # Datos específicos para Company
    legal_agent = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    business_vertical = models.CharField(max_length=100, blank=True, null=True)
    company_type = models.CharField(max_length=100, blank=True, null=True)

class Project(models.Model):

    STATE_CHOICES = [
        ('PENDING', 'Finding freelancers'),
        ('IN_PROGRESS', 'Developing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    # Información básica del proyecto
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    budget = models.DecimalField(max_digits=10, decimal_places=2) 
    type = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    url = models.URLField()
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default='PENDING')
    project_picture = models.ImageField(upload_to='project_pictures/', blank=True, null=True)
    manager = models.ForeignKey(CompanyManager, on_delete=models.PROTECT, related_name='managed_projects', null=True)

    # Elementos del proyecto
    requirements = models.ManyToManyField('Requirement', related_name='projects', blank=True)
    milestones = models.ManyToManyField('Milestone', related_name='projects', blank=True)
    tasks = models.ManyToManyField('Task', related_name='projects', blank=True)

    def __str__(self):
        return self.name

class Requirement(models.Model):
    # Requisitos para el proyecto
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title

class Milestone(models.Model):
    # Hitos del proyecto
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    deadline = models.DateField()

    def __str__(self):
        return self.title

class Task(models.Model):
    # Tareas individuales dentro de hitos y proyectos
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    deadline = models.DateField()
    assigned_freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='tasks', null=True)

    def __str__(self):
        return self.title

class Experience(models.Model):
    # Experiencia de los freelancers
    company_name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=1000)
    freelancer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='experiences')

    def __str__(self):
        return f"{self.job} at {self.company_name}"

class Portfolio(models.Model):
    # Portafolio del freelancer
    freelancer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='portfolios')

class Content(models.Model):
    # Contenidos en el portafolio
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=300)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.PROTECT, related_name='contents')

class Rate(models.Model):
    # Calificación de freelancer
    value = models.DecimalField(max_digits=3, decimal_places=1)
    date = models.DateField(default=timezone.now)
    comment = models.CharField(max_length=200)
    freelancer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='rates')

class Publication(models.Model):
    # Publicaciones de proyectos por parte de una compañía
    date = models.DateField()
    company_manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='publications', null=True)

class Contract(models.Model):
    # Contratos entre freelancers y compañías
    date = models.DateField()
    company_manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contracts_as_manager', null=True)
    freelancer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contracts_as_freelancer', null=True)

class Payment(models.Model):
    # Pagos de la compañía al freelancer
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    company_manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments_made', null=True)
    freelancer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments_received', null=True)

class Application(models.Model):
    # Aplicación de freelancers a proyectos
    date = models.DateField(default=timezone.now)
    freelancer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')

class Reference(models.Model):
    # Referencias de experiencias previas
    position = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    experience = models.ForeignKey(Experience, on_delete=models.PROTECT, related_name='references')

class Chat(models.Model):
    # Sistema de mensajería básica
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
