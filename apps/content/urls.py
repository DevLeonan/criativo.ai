from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('historico/', views.history, name='history'),
    path('ajustes/', views.settings_view, name='settings'), # A nova rota de ajustes!
    path('checkout/', views.checkout, name='checkout'),
]