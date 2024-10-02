from django.db import models
from my_aplication.models import Freelancer, User
from perfil.models import Project
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

# class Project(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=500)
#     budget = models.DecimalField(max_digits=10, decimal_places=2) 
#     deadline = models.DateField()
    
    #Unión con el modelo de Project de la aplicación de perfil... No pueden existir 2 modelos con el mismo nombre
    #A menos de que se extienda o se importe del modelo de la aplicación de perfil

class Requirement(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='requirements')

class Milestone(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    deadline = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='milestones')

class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    deadline = models.DateField()
    milestone = models.ForeignKey(Milestone, on_delete=models.PROTECT, related_name='tasks')
    freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='tasks')

class Comment(models.Model):
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    user = GenericForeignKey('content_type', 'object_id')
    comment = models.ForeignKey('self', on_delete=models.PROTECT, related_name='replies', null=True, blank=True) # can have a reply

# Esperando a discutir en qué modelo se va a guardar el rating  
# class Rating(models.Model):
#     value = models.DecimalField(max_digits=3, decimal_places=1)
#     project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='ratings')
#     content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
#     object_id = models.PositiveIntegerField()
#     user = GenericForeignKey('content_type', 'object_id')