from rest_framework import viewsets

from apps.produtos.models import Produto
from apps.produtos.serializers import ProdutoSerializer


class ProdutoViewSet(viewsets.ModelViewSet):

    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    search_fields = ['nome', 'codigo', 'categoria']
    ordering_fields = ['nome', 'codigo', 'data_cadastro']
