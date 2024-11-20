from django.urls import path

from . import views
urlpatterns = [
    path('home/<str:id>/', views.home, name='home'),
    path('', views.home, name='home'),
]