from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('perfilesFreelancer/<int:id>/', views.perfilesFreelancer, name='perfilFreelancer'),
    path('perfilesCliente/<int:id>/', views.perfilesCliente, name='perfilesCliente'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)