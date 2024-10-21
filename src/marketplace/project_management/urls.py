from django.urls import path
from . import views
from my_aplication.models import Rate

urlpatterns = [
        #Recomendaciones para urls:
        path('freelancer_project/', views.freelancerProjectView2, name='freelancer_project2'),
        path('freelancer_project/<int:id>/', views.freelancerProjectView, name='freelancer_project'),
        path('client_project/<int:id>/', views.clientProjectView, name='client_project'),
]