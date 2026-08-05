from rest_framework import viewsets

from apps.ia.models import ModeloIA
from apps.ia.serializers import ModeloIASerializer


class ModeloIAViewSet(viewsets.ModelViewSet):

    queryset = ModeloIA.objects.all()
    serializer_class = ModeloIASerializer
    search_fields = ['nome', 'versao']
    ordering_fields = ['nome', 'data_cadastro']
