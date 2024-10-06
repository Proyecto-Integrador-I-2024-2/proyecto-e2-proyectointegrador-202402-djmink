from django.db import models

from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    jobs_completed = models.IntegerField(default=0)
    price = models.CharField(max_length=100)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class ClientProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField(default=0.0)

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
    profile = models.ForeignKey(ClientProfile, related_name='projects', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name