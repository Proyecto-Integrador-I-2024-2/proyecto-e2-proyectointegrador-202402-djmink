from django.urls import path
from . import views

urlpatterns = [
    path('notifications/<int:id>/', views.notifications, name='notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
]
