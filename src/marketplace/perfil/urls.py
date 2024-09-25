from django.urls import path
from . import views

urlpatterns = [
    # path ('perfiles/', views.perfiles, name='perfiles'),
    path('perfiles/<int:user_id>/', views.perfil, name='perfil'),
]