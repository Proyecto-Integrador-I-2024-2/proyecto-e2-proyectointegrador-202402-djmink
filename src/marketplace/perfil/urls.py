from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('perfilesFreelancer/<int:id>/', views.perfilesFreelancer, name='perfilFreelancer'),
    path('perfilesCliente/<int:id>/', views.perfilesCliente, name='perfilesCliente'),
    path('perfilesCliente/<int:id>/main/', views.mainCliente, name='mainCliente'),
    path('perfilesFreelancer/<int:id>/main/', views.mainFreelancer, name='mainFreelancer'),
    path('perfilesFreelancer/<int:id>/account/', views.editAccount, name='editAccount'),
    path('perfilesFreelancer/<int:id>/editProfile/', views.editProfile, name='editProfile'),
    path('perfilesFreelancer/<int:id>/delete&disable/', views.deleteDisable, name='deleteDisable'),
    path('perfilesFreelancer/<int:id>/portfolio/', views.editPortfolio, name='editPortfolio'),
    path('perfilesFreelancer/<int:id>/projects/', views.projectsList, name='projectsList'),
    path('perfilesFreelancer/<int:id>/projects/<int:id_project>/', views.projectWorkspace, name='projectWorkspace'),
    path('home/publications/', views.firstMain, name='firstMain'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)