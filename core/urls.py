from django.contrib import admin
from django.urls import path, include
from . import views # Importa a view que acabamos de criar

urlpatterns = [
    path('admin/', admin.site.models.admin_site.urls if hasattr(admin.site, 'models') else admin.site.urls),
    path('', views.home, name='landing_page'), # A Rota da Landing Page!
    path('', include('apps.accounts.urls')), 
    path('', include('apps.content.urls')),  
]