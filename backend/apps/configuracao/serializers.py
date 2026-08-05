from rest_framework import serializers

from apps.configuracao.models import Camera, Etapa, Linha, Workflow


class LinhaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Linha
        fields = [
            'id',
            'nome',
            'codigo',
            'descricao',
            'produto',
            'ativo',
            'data_cadastro',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'data_cadastro', 'atualizado_em']


class CameraSerializer(serializers.ModelSerializer):

    class Meta:
        model = Camera
        fields = [
            'id',
            'nome',
            'identificador',
            'tipo',
            'linha',
            'ativo',
            'data_cadastro',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'data_cadastro', 'atualizado_em']


class EtapaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Etapa
        fields = ['id', 'workflow', 'ordem', 'tipo', 'ativo']
        read_only_fields = ['id']


class WorkflowSerializer(serializers.ModelSerializer):

    etapas = EtapaSerializer(many=True, read_only=True)

    class Meta:
        model = Workflow
        fields = [
            'id',
            'nome',
            'descricao',
            'produto',
            'etapas',
            'ativo',
            'data_cadastro',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'data_cadastro', 'atualizado_em']
