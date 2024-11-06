from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, null=True)

    description = models.TextField()
    rating = models.FloatField(default=0.0)
    contact_email = models.CharField(max_length=100, default='example@example.com')
    date_joined = models.DateField(default=timezone.now)

    REQUIRED_FIELDS = ['email']  # Campos requeridos al crear un usuario
    USERNAME_FIELD = 'username'

    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

class Freelancer(User):
    EXPERIENCE_CHOICES = [
        ('junior', 'Junior'),
        ('semi_senior', 'Semi-senior'),
        ('senior', 'Senior'),
        ('manager', 'Manager'),
        ('lead', 'Lead'),
    ]

    profession = models.CharField(max_length=100)
    identification = models.CharField(max_length=100, blank=True, null=True)
    jobs_completed = models.IntegerField(default=0)
    price = models.CharField(max_length=100)
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='junior')

class CompanyManager(User):
    legal_agent = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    business_vertical = models.CharField(max_length=100, blank=True, null=True)
    company_type = models.CharField(max_length=100, blank=True, null=True)

class Rating(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    user = GenericForeignKey('content_type', 'object_id')
    score = models.FloatField()
    date_rated = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.rated_by} rated {self.user} - {self.score}'

class Skill(models.Model):
    profile = models.ForeignKey(Freelancer, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Certificate(models.Model):
    profile = models.ForeignKey(Freelancer, related_name='certificates', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name
    
class CommentProfile(models.Model):
    user_profile = models.ForeignKey(User, related_name="comments_received", on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, related_name="comments_made", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name="replies", null=True, blank=True
    )

    def __str__(self):
        return f"{self.author} on {self.user_profile}: {self.content[:20]}" 
    

class Project(models.Model):

    STATE_CHOICES = [
        ('PENDING', 'Finding freelancers'),
        ('IN_PROGRESS', 'Developing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    manager = models.ForeignKey(CompanyManager, related_name='projects', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Untitled Project')  # Default project name
    type = models.CharField(max_length=100, default='General')  # Default type
    duration = models.CharField(max_length=100, default='Not Specified')  # Default duration
    description = models.TextField(default='No description provided.')  # Default description
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default budget
    deadline = models.DateField(null=True, blank=True)  # No default, but can be left empty
    date_created = models.DateField(auto_now_add=True)  # Automatically set to the current date when created
    project_picture = models.ImageField(upload_to='project_pictures/', blank=True, null=True)
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default='PENDING')
    

    def _str_(self):
        return self.name
    
class Like(models.Model):
    project = models.ForeignKey(Project, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    user = GenericForeignKey('content_type', 'object_id')

    def _str_(self):
        return f"{self.user} likes {self.project}"
    
class ProjectComment(models.Model):
    author = models.CharField(max_length=100, default='Anonymous')
    content = models.TextField(default='No content provided.')
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    user = GenericForeignKey('content_type', 'object_id')
    comment = models.ForeignKey('self', on_delete=models.PROTECT, related_name='replies', null=True, blank=True)  # can have a reply

class SocialNetwork(models.Model):

    TYPE_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
    ]

    profile = models.ForeignKey(Freelancer, related_name='social_networks', on_delete=models.CASCADE, null=True, blank=True)
    client_profile = models.ForeignKey(CompanyManager, related_name='client_social_networks', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, unique=True)
    url = models.CharField(max_length=255)
    image = models.ImageField(upload_to='social_networks/', default='social_networks/default_icon.png')

    def save(self, *args, **kwargs):
        if self.image.name == 'social_networks/default_icon.png':
            if self.type == 'facebook':
                self.image = 'social_networks/facebook_icon.png'
            elif self.type == 'twitter':
                self.image = 'social_networks/twitter_icon.jpg'
            elif self.type == 'instagram':
                self.image = 'social_networks/instagram_icon.png'
            elif self.type == 'linkedin':
                self.image = 'social_networks/linkedin_icon.png'
            elif self.type == 'github':
                self.image = 'social_networks/github_icon.png'
        super().save(*args, **kwargs)

class ProjectCategory(models.Model):
    project = models.ForeignKey(Project, related_name='projectcategories', on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)


class ProjectRating(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='ratings')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    user = GenericForeignKey('content_type', 'object_id')

class SavedProject(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    user_id = models.PositiveIntegerField()
    user = GenericForeignKey('content_type', 'user_id')
    project = models.ForeignKey(Project, related_name='saved_projects', on_delete=models.CASCADE)

class Milestone(models.Model):

    STATE_CHOICES = [
        ('Available', 'available'),
        ('Taken', 'taken'),
    ]

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField() 
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='milestones')
    progress = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='milestones')
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default='Available')

class Profession(models.Model):
    requeriment = models.ForeignKey(Milestone, related_name='professions', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Task(models.Model):

    STATE_CHOICES = [
        ('NS', 'Not started'),
        ('IP', 'In Progress'),
        ('CP', 'Completed'),
    ]

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    deadline = models.DateField()
    milestone = models.ForeignKey(Milestone, on_delete=models.PROTECT, related_name='tasks')
    freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='tasks')
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default='NS')

class Assignment(models.Model):
    project = models.ForeignKey(Project, related_name='assignments', on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    date = models.DateField()
    status = models.CharField(max_length=50)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

class Content(models.Model):
    profile = models.ForeignKey(Freelancer, related_name='contents', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

class Application(models.Model):
    STATE_CHOICES = [
        ('Sent', 'sent'),
        ('Approved', 'approved'),
        ('Rejected', 'rejected'),
    ]
    date = models.DateField(auto_now_add=True)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='applications')
    accepted = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='applications')
    milestone = models.ForeignKey(Milestone, on_delete=models.PROTECT, related_name='applications')
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default='Sent')

#Los del modelo pero que no usamos

class Experience(models.Model):
    # Experiencia de los freelancers
    company_name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=1000)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='experiences')

    def __str__(self):
        return f"{self.job} at {self.company_name}"

class Portfolio(models.Model):
    # Portafolio del freelancer
    freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='portfolios')

class Publication(models.Model):
    # Publicaciones de proyectos por parte de una compañía
    date = models.DateField()
    company_manager = models.ForeignKey(CompanyManager, on_delete=models.PROTECT, related_name='publications', null=True)

class Contract(models.Model):
    # Contratos entre freelancers y compañías
    date = models.DateField()
    company_manager = models.ForeignKey(CompanyManager, on_delete=models.PROTECT, related_name='contracts_as_manager', null=True)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='contracts_as_freelancer', null=True)

class Payment(models.Model):
    # Pagos de la compañía al freelancer
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    company_manager = models.ForeignKey(CompanyManager, on_delete=models.PROTECT, related_name='payments_made', null=True)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='payments_received', null=True)


class Reference(models.Model):
    # Referencias de experiencias previas
    position = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    experience = models.ForeignKey(Experience, on_delete=models.PROTECT, related_name='references')
