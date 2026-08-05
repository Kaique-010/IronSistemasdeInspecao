from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import IndexView
from apps.produtos.urls import router as produtos_router
from apps.configuracao.urls import router as configuracao_router
from apps.ia.urls import router as ia_router

api_router = DefaultRouter()
api_router.registry.extend(produtos_router.registry)
api_router.registry.extend(configuracao_router.registry)
api_router.registry.extend(ia_router.registry)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('tenant/', include('apps.tenants.urls')),
    path('api/', include(api_router.urls)),
    path('<slug:tenant_slug>/', include('apps.tenants.urls_tenant')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
