import pytest
from rest_framework.test import APIClient

from apps.ia.models import ModeloIA


@pytest.mark.django_db
def test_criar_modelo_ia():

    modelo = ModeloIA.objects.create(
        nome="YOLOv8",
        tipo=ModeloIA.TipoModelo.DETECTOR,
        versao="1.0",
    )

    assert str(modelo) == "YOLOv8 v1.0"


@pytest.mark.django_db
def test_nome_versao_modelo_unico():

    ModeloIA.objects.create(nome="YOLOv8", versao="1.0")

    with pytest.raises(Exception):
        ModeloIA.objects.create(nome="YOLOv8", versao="1.0")


@pytest.mark.django_db
def test_api_listar_modelos():

    ModeloIA.objects.create(nome="RT-DETR", versao="2.0")

    client = APIClient()
    response = client.get("/api/modelos/")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["nome"] == "RT-DETR"


@pytest.mark.django_db
def test_api_criar_modelo():

    client = APIClient()
    response = client.post(
        "/api/modelos/",
        {
            "nome": "Grounding DINO",
            "tipo": "detector",
            "versao": "1.1",
            "descricao": "Detector open-set",
        },
        format="json",
    )

    assert response.status_code == 201
    assert ModeloIA.objects.count() == 1
