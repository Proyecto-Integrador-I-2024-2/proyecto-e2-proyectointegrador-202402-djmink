from django.urls import path
from . import views

urlpatterns = [
    path('perfil/<int:profile_id>/', views.perfil, name='perfil'),
]