from django.db import models
from my_aplication import Freelancer

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    budget = models.DecimalField(max_digits=10, decimal_places=2) 
    deadline = models.DateField()

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