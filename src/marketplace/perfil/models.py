from django.db import models

from django.db import models

class Profile(models.Model):

    EXPERIENCE_CHOICES = [
        ('junior', 'Junior'),
        ('semi_senior', 'Semi-senior'),
        ('senior', 'Senior'),
        ('manager', 'Manager'),
        ('lead', 'Lead'),
    ]
     
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    jobs_completed = models.IntegerField(default=0)
    price = models.CharField(max_length=100)
    join_date = models.DateField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    contact_email = models.CharField(max_length=100, default='example@example.com')
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='junior')

    def __str__(self):
        return self.name

class ClientProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    profile = models.ForeignKey(Profile, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Certificate(models.Model):
    profile = models.ForeignKey(Profile, related_name='certificates', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

class Comment(models.Model):
    profile = models.ForeignKey(Profile, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.content}"

class CommentClient(models.Model):
    profile = models.ForeignKey(ClientProfile, related_name='commentsClients', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.content}"

class Content(models.Model):
    profile = models.ForeignKey(Profile, related_name='contents', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

class Project(models.Model):

    STATE_CHOICES = [
        ('PENDING', 'Finding freelancers'),
        ('IN_PROGRESS', 'Developing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    profile = models.ForeignKey(ClientProfile, related_name='projects', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    url = models.URLField()
    description = models.CharField(max_length=500, default='Description')
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default='PENDING')
    project_picture = models.ImageField(upload_to='project_pictures/', blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class ProjectFreelancer(models.Model):

    STATE_CHOICES = [
        ('PENDING', 'Finding freelancers'),
        ('IN_PROGRESS', 'Developing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    profile = models.ForeignKey(Profile, related_name='projects', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    #type = models.CharField(max_length=100)
    #duration = models.CharField(max_length=100)
    #url = models.URLField()
    description = models.CharField(max_length=500, default='Description')
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default='PENDING')
    project_picture = models.ImageField(upload_to='project_pictures/', blank=True, null=True)
    #budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name




class Publication(models.Model):
    profile = models.ForeignKey(ClientProfile, related_name='publications', on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, related_name='publications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    favorites = models.IntegerField()


class CommentPublication(models.Model):
    publication = models.ForeignKey(Publication, related_name='commentsPublication', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.content}"
    
class Requirement(models.Model):

    STATE_CHOICES = [
        ('Available', 'available'),
        ('Taken', 'available'),
    ]

    project = models.ForeignKey(Project, related_name='requirements', on_delete=models.CASCADE) 
    description = models.CharField(max_length=500, default='Description')
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default='Available')

class Profession(models.Model):
    requeriment = models.ForeignKey(Requirement, related_name='professions', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class ProjectCategory(models.Model):
    project = models.ForeignKey(Project, related_name='projectcategories', on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)


class SocialNetwork(models.Model):

    TYPE_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
    ]

    profile = models.ForeignKey(Profile, related_name='social_networks', on_delete=models.CASCADE, null=True, blank=True)
    client_profile = models.ForeignKey(ClientProfile, related_name='client_social_networks', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, unique=True)
    url = models.URLField(max_length=200)
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

    def __str__(self):
        return self.type

class Milestone(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    deadline = models.DateField()
    project = models.ForeignKey(ProjectFreelancer, on_delete=models.PROTECT, related_name='milestones')

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    deadline = models.DateField()
    milestone = models.ForeignKey(Milestone, on_delete=models.PROTECT, related_name='tasks')
    freelancer = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='tasks')

class Assignment(models.Model):
    name = models.CharField(max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    date = models.DateField()
    status = models.CharField(max_length=50)
    file = models.FileField(upload_to='uploads/')
    url = models.URLField(blank=True, null=True)
