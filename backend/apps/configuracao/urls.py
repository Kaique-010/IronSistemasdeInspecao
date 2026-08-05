from rest_framework.routers import DefaultRouter

from apps.configuracao.views import (
    CameraViewSet,
    EtapaViewSet,
    LinhaViewSet,
    WorkflowViewSet,
)

router = DefaultRouter()
router.register('linhas', LinhaViewSet, basename='linha')
router.register('cameras', CameraViewSet, basename='camera')
router.register('workflows', WorkflowViewSet, basename='workflow')
router.register('etapas', EtapaViewSet, basename='etapa')

urlpatterns = router.urls
