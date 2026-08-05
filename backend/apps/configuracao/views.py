from rest_framework import viewsets

from apps.configuracao.models import Camera, Etapa, Linha, Workflow
from apps.configuracao.serializers import (
    CameraSerializer,
    EtapaSerializer,
    LinhaSerializer,
    WorkflowSerializer,
)


class LinhaViewSet(viewsets.ModelViewSet):

    queryset = Linha.objects.all()
    serializer_class = LinhaSerializer
    search_fields = ['nome', 'codigo']
    ordering_fields = ['nome', 'codigo', 'data_cadastro']


class CameraViewSet(viewsets.ModelViewSet):

    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    search_fields = ['nome', 'identificador']
    ordering_fields = ['nome', 'data_cadastro']


class WorkflowViewSet(viewsets.ModelViewSet):

    queryset = Workflow.objects.prefetch_related('etapas')
    serializer_class = WorkflowSerializer
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_cadastro']


class EtapaViewSet(viewsets.ModelViewSet):

    queryset = Etapa.objects.all()
    serializer_class = EtapaSerializer
    ordering_fields = ['workflow', 'ordem']
