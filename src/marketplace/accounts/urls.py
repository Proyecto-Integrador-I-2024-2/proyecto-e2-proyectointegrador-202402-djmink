from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('recover/', views.recover, name='recover'),
    path('recover/confirmation', views.recover_confirmation, name='recover_confirmation'),
    path('register/freelancer1', views.registerf1, name='registerf1'),
    path('register/freelancer2/<int:id>', views.registerf2, name='registerf2'),
    path('register/freelancer3/<int:id>', views.registerf3, name='registerf3'),
    path('register/company1', views.registerc1, name='registerc1'),
    path('register/company2/<int:id>', views.registerc2, name='registerc2'),
    path('client/addproject/', views.addproject, name='addproject'),
    path('client/<int:id>/create-project', views.create_project_view, name='create_project'),
    path('post_project/', views.post_project, name='post_project'),
    path('client/<int:id_client>/edit-project/<int:id_project>/', views.edit_project_view, name='edit_project'),
    path('post_project_edition/<int:id>/', views.post_project_edition, name='post_project_edition'),
    path('editproject/', views.editproject, name='editproject'),

]