import pytest
from rest_framework.test import APIClient

from apps.produtos.models import Produto


@pytest.mark.django_db
def test_criar_produto():

    produto = Produto.objects.create(
        nome="Abacaxi Pérola",
        codigo="SKU-001",
        categoria="Fruta",
    )

    assert produto.codigo == "SKU-001"
    assert produto.ativo is True
    assert str(produto) == "SKU-001 - Abacaxi Pérola"


@pytest.mark.django_db
def test_codigo_produto_unico():

    Produto.objects.create(nome="Abacaxi", codigo="SKU-001")

    with pytest.raises(Exception):
        Produto.objects.create(nome="Abacaxi 2", codigo="SKU-001")


@pytest.mark.django_db
def test_api_listar_produtos():

    Produto.objects.create(nome="Tomate", codigo="SKU-002")

    client = APIClient()
    response = client.get("/api/produtos/")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["codigo"] == "SKU-002"


@pytest.mark.django_db
def test_api_criar_produto():

    client = APIClient()
    response = client.post(
        "/api/produtos/",
        {"nome": "Laranja", "codigo": "SKU-003", "categoria": "Fruta"},
        format="json",
    )

    assert response.status_code == 201
    assert Produto.objects.count() == 1


@pytest.mark.django_db
def test_api_buscar_produto():

    produto = Produto.objects.create(nome="Maçã", codigo="SKU-004")

    client = APIClient()
    response = client.get(f"/api/produtos/{produto.id}/")

    assert response.status_code == 200
    assert response.data["nome"] == "Maçã"


@pytest.mark.django_db
def test_api_editar_produto():

    produto = Produto.objects.create(nome="Maçã", codigo="SKU-005")

    client = APIClient()
    response = client.patch(
        f"/api/produtos/{produto.id}/",
        {"nome": "Maçã Gala"},
        format="json",
    )

    assert response.status_code == 200
    produto.refresh_from_db()
    assert produto.nome == "Maçã Gala"


@pytest.mark.django_db
def test_api_deletar_produto():

    produto = Produto.objects.create(nome="Batata", codigo="SKU-006")

    client = APIClient()
    response = client.delete(f"/api/produtos/{produto.id}/")

    assert response.status_code == 204
    assert Produto.objects.count() == 0
