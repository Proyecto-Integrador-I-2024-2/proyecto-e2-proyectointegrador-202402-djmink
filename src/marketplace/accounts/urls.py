from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='signup'),  # Añade esta línea
    path('register/company/', views.register_company, name='register_company'),
    path('register/freelancer/', views.register_freelancer, name='register_freelancer'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registration_success/', views.registration_success, name='registration_success'),
]
