from django.contrib.auth import get_user_model

from core.tenant_context import setar_tenant_atual

from apps.configuracao.models import Etapa, Linha, Workflow
from apps.ia.models import ModeloIA
from apps.produtos.models import Produto
from apps.tenants.models import Empresa, MembroEmpresa


empresa = Empresa.objects.get(slug="empresa-demonstracao")

usuario = get_user_model().objects.get(username="leosousa")

MembroEmpresa.objects.get_or_create(
    usuario=usuario,
    empresa=empresa,
    defaults={
        "papel": MembroEmpresa.Papel.ADMIN,
        "ativo": True,
    },
)

setar_tenant_atual(empresa)

produto, _ = Produto.objects.get_or_create(
    codigo="ABACAXI-001",
    defaults={
        "nome": "Abacaxi",
        "descricao": "Abacaxi in natura",
        "categoria": "Fruta",
        "ativo": True,
    },
)

workflow, _ = Workflow.objects.get_or_create(
    nome="Workflow Abacaxi",
    defaults={
        "produto": produto,
        "descricao": "Detecção de abacaxi na esteira",
        "ativo": True,
    },
)

linha, _ = Linha.objects.get_or_create(
    codigo="LINHA-ABACAXI",
    defaults={
        "nome": "Linha Abacaxi",
        "produto": produto,
        "ativo": True,
    },
)

Etapa.objects.get_or_create(
    workflow=workflow,
    ordem=1,
    defaults={
        "tipo": Etapa.TipoEtapa.DETECCAO,
        "ativo": True,
    },
)

modelo, _ = ModeloIA.objects.get_or_create(
    nome="Detector Abacaxi/Tomate",
    versao="v1",
    defaults={
        "tipo": ModeloIA.TipoModelo.DETECTOR,
        "arquivo": "runs/detect/abacaxi_tomate/weights/best.pt",
        "descricao": "YOLOv8n treinado em 1129 imagens (abacaxi + tomate)",
        "ativo": True,
    },
)

print("produto:", produto)
print("workflow:", workflow)
print("linha:", linha)
print("modelo:", modelo)
print("membro:", MembroEmpresa.objects.filter(empresa=empresa).count())
