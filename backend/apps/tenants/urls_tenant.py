from django.urls import path
from . import views

urlpatterns = [
    path('', views.TenantHomeView.as_view(), name='tenant_home'),
    path('detectar/', views.detectar, name='tenant_detectar'),
]
