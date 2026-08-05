from rest_framework.routers import DefaultRouter

from apps.ia.views import ModeloIAViewSet

router = DefaultRouter()
router.register('modelos', ModeloIAViewSet, basename='modelo-ia')

urlpatterns = router.urls
