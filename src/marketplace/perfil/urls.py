from django.urls import path
from . import views

urlpatterns = [
    path('perfilesFreelancer/<int:freelancer_profile_id>/', views.perfilesFreelancer, name='perfilFreelancer'),
    path('perfilesCliente/<int:company_profile_id>/', views.perfilesCliente, name='perfilesCliente'),
]