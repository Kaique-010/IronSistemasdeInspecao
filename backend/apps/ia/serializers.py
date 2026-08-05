from rest_framework import serializers

from apps.ia.models import ModeloIA


class ModeloIASerializer(serializers.ModelSerializer):

    class Meta:
        model = ModeloIA
        fields = [
            'id',
            'nome',
            'tipo',
            'versao',
            'arquivo',
            'descricao',
            'ativo',
            'data_cadastro',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'data_cadastro', 'atualizado_em']
