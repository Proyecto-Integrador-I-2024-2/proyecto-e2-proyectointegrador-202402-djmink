from django.contrib import admin

from my_aplication.models import Application, User, CommentProfile, Freelancer, CompanyManager, Skill, Certificate, Content, Project, Publication, Profession, ProjectCategory, SocialNetwork, Milestone, Task, Assignment

admin.site.register(User)
admin.site.register(Freelancer)
admin.site.register(CompanyManager)
admin.site.register(Skill)
admin.site.register(Certificate)
admin.site.register(CommentProfile)
admin.site.register(Content)
admin.site.register(Project)
admin.site.register(Publication)
admin.site.register(Profession)
admin.site.register(ProjectCategory)
admin.site.register(SocialNetwork)
admin.site.register(Milestone)
admin.site.register(Task)
admin.site.register(Assignment)
admin.site.register(Application)