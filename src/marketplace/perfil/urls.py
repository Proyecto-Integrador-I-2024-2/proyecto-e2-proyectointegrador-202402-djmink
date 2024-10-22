from django.urls import path
from . import views

urlpatterns = [
    path('perfilesFreelancer/<int:id>/', views.perfilesFreelancer, name='perfilFreelancer'),
    path('perfilesCliente/<int:id>/', views.perfilesCliente, name='perfilesCliente'),
]