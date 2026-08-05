from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.tenant_test, name='tenant_test'),
    path('trocar/', views.trocar_tenant, name='trocar_tenant'),
    path('minhas/', views.minhas_empresas, name='minhas_empresas'),
]
