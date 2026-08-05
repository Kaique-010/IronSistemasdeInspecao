import pytest
from rest_framework.test import APIClient

from apps.configuracao.models import Camera, Etapa, Linha, Workflow
from apps.produtos.models import Produto


@pytest.mark.django_db
def test_criar_linha():

    produto = Produto.objects.create(nome="Abacaxi", codigo="SKU-L1")

    linha = Linha.objects.create(
        nome="Esteira 1",
        codigo="LIN-01",
        produto=produto,
    )

    assert str(linha) == "LIN-01 - Esteira 1"
    assert linha.produto == produto


@pytest.mark.django_db
def test_criar_camera_vinculada_a_linha():

    linha = Linha.objects.create(nome="Esteira 1", codigo="LIN-02")

    camera = Camera.objects.create(
        nome="Câmera Topo",
        identificador="192.168.0.10",
        linha=linha,
    )

    assert camera.tipo == Camera.TipoCamera.IP
    assert camera.linha == linha


@pytest.mark.django_db
def test_criar_workflow_com_etapas():

    produto = Produto.objects.create(nome="Tomate", codigo="SKU-W1")

    workflow = Workflow.objects.create(
        nome="Padrão Tomate",
        produto=produto,
    )

    Etapa.objects.create(workflow=workflow, ordem=1, tipo=Etapa.TipoEtapa.DETECCAO)
    Etapa.objects.create(workflow=workflow, ordem=2, tipo=Etapa.TipoEtapa.CLASSIFICACAO)
    Etapa.objects.create(workflow=workflow, ordem=3, tipo=Etapa.TipoEtapa.DESTINO)

    assert workflow.etapas.count() == 3
    assert list(workflow.etapas.values_list('ordem', flat=True)) == [1, 2, 3]


@pytest.mark.django_db
def test_api_workflow_retorna_etapas():

    produto = Produto.objects.create(nome="Laranja", codigo="SKU-W2")

    workflow = Workflow.objects.create(
        nome="Padrão Laranja",
        produto=produto,
    )

    Etapa.objects.create(workflow=workflow, ordem=1, tipo=Etapa.TipoEtapa.DETECCAO)

    client = APIClient()
    response = client.get(f"/api/workflows/{workflow.id}/")

    assert response.status_code == 200
    assert response.data["etapas"][0]["tipo"] == "deteccao"


@pytest.mark.django_db
def test_api_criar_linha():

    client = APIClient()
    response = client.post(
        "/api/linhas/",
        {"nome": "Esteira 2", "codigo": "LIN-03"},
        format="json",
    )

    assert response.status_code == 201
    assert Linha.objects.count() == 1


@pytest.mark.django_db
def test_api_criar_camera():

    linha = Linha.objects.create(nome="Esteira 2", codigo="LIN-04")

    client = APIClient()
    response = client.post(
        "/api/cameras/",
        {"nome": "Câmera Lado", "identificador": "cam-01", "linha": linha.id},
        format="json",
    )

    assert response.status_code == 201
    assert Camera.objects.count() == 1
