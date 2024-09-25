from django.contrib import admin

from .models import Profile, Skill, Certificate, Comment, Content, ClientProfile, Project, CommentClient

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Certificate)
admin.site.register(Comment)
admin.site.register(Content)
admin.site.register(ClientProfile)
admin.site.register(Project)
admin.site.register(CommentClient)

