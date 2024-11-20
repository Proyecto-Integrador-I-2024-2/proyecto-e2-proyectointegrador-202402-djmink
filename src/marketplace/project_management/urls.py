from django.urls import path
from . import views

urlpatterns = [
        #Recomendaciones para urls:
        path('freelancer_project/', views.freelancerProjectView2, name='freelancer_project2'),
        path('freelancer_project/<int:freelancer_id>/<int:id>/', views.freelancerProjectView, name='freelancer_project'),
        path('client_project/<int:id>/', views.clientProjectView, name='client_project'),
        path('post_comment/', views.post_comment, name='post_comment'),
        path('post_application/', views.post_application, name='post_application'),
        path('post_like/', views.post_like, name='post_like'),
        path('post_saved/', views.post_saved, name='post_saved'),
]