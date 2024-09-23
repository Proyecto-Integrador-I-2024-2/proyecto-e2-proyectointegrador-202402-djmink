from django.urls import path

from . import views
urlpatterns = [
    path('', views.users, name='users'),
    path('register/', views.register, name='register'),
    path('complete/<int:profile_id>/', views.complete, name='complete'),
    path('home/', views.home, name='home'),

]