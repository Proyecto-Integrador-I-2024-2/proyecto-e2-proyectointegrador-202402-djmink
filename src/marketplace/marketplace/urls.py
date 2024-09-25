from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Incluye las URLs de django-allauth para login, logout, registro, etc.
    path('accounts/', include('allauth.urls')),

    # Incluye las URLs de tu aplicación personalizada
    path('', include('accounts.urls')),
]
