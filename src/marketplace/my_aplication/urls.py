from django.urls import path

from . import views
urlpatterns = [
    path('users/', views.users, name='users'),
    path('register/', views.register, name='register'),
    path('complete/<int:profile_id>/', views.complete, name='complete'),

    path('', views.home, name='home'),

]