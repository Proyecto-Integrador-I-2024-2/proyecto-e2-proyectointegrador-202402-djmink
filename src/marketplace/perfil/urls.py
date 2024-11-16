from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #en todas falta linkear los del footer
    path('home/publications/', views.firstMain, name='firstMain'), #solo falta linkear con login y signup
    #freelancer
    path('freelancer/<int:id>/', views.perfilesFreelancer, name='perfilFreelancer'),
    path('freelancer/<int:id>/home/', views.mainFreelancer, name='mainFreelancer'),
    path('freelancer/<int:id>/account/', views.editAccount, name='editAccount'),
    path('freelancer/<int:id>/editProfile/', views.editProfile, name='editProfile'),
    path('freelancer/<int:id>/delete&disable/', views.deleteDisable, name='deleteDisable'),
    path('freelancer/<int:id>/portfolio/', views.editPortfolio, name='editPortfolio'),
    path('freelancer/<int:id>/projects/', views.projectsList, name='projectsList'),
    path('freelancer/<int:id>/projects/<int:id_project>/', views.projectWorkspace, name='projectWorkspace'),
    path('freelancer/<int:id>/view-profile/<int:idclient>/', views.clientProfile, name='clientProfile'),
    
    #cliente
    path('client/<int:id>/', views.perfilesCliente, name='perfilesCliente'),
    path('client/<int:id>/home/', views.mainCliente, name='mainCliente'),
    path('client/<int:id>/delete&disable/', views.deleteDisableClient, name='deleteDisableClient'),
    path('client/<int:id>/edit-projects/', views.editProjectsClient, name='editProjectsClient'),
    path('client/<int:id>/editProfile/', views.editProfileClient, name='editProfileClient'),
    path('client/<int:id>/account/', views.editAccountClient, name='editAccountClient'),
    path('client/<int:idclient>/view-profile/<int:id>/', views.freelancerProfile, name='freelancerProfile'),
    path('client/<int:id>/manage-project/<int:id_project>/', views.manageProject, name='manageProject'),

    #para ver el perfil del freelancer
    # urls.py
    

    


    #calendar
    path('calendar/', views.calendar, name='calendar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)