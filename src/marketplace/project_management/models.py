from django.db import models
from my_aplication.models import Freelancer, User, Requirement
from perfil.models import Project
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Milestone(models.Model):
    title = models.CharField(max_length=50, default='New Milestone')
    description = models.CharField(max_length=500, default='No description provided.')
    deadline = models.DateField(auto_now_add=False, default=None)  # Set a default date as needed
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='milestones')

class Task(models.Model):
    title = models.CharField(max_length=50, default='New Task')
    description = models.CharField(max_length=500, default='No description provided.')
    deadline = models.DateField(auto_now_add=False, default=None)  # Set a default date as needed
    milestone = models.ForeignKey(Milestone, on_delete=models.PROTECT, related_name='tasks')
    freelancer = models.ForeignKey(Freelancer, on_delete=models.PROTECT, related_name='tasks')

class ProjectComment(models.Model):
    author = models.CharField(max_length=100, default='Anonymous')
    content = models.TextField(default='No content provided.')
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    user = GenericForeignKey('content_type', 'object_id')
    comment = models.ForeignKey('self', on_delete=models.PROTECT, related_name='replies', null=True, blank=True)  # can have a reply

class Rating(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='ratings')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    user = GenericForeignKey('content_type', 'object_id')