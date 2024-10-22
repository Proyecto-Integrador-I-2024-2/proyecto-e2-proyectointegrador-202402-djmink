from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('recover/', views.recover, name='recover'),
    path('recover/confirmation', views.recover_confirmation, name='recover_confirmation'),

]

