from rest_framework import serializers

from apps.produtos.models import Produto


class ProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produto
        fields = [
            'id',
            'nome',
            'codigo',
            'descricao',
            'categoria',
            'ativo',
            'data_cadastro',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'data_cadastro', 'atualizado_em']
