from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.tenant_test, name='tenant_test'),
]
