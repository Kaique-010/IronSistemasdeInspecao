import pytest

from django.contrib.sessions.backends.db import SessionStore

from apps.tenants.middleware import TenantMiddleware
from apps.tenants.models import Empresa


class RequisicaoFalsa:
    def __init__(self, caminho, headers=None):
        self.path_info = caminho
        self.headers = headers or {}
        self.session = SessionStore()


@pytest.mark.django_db
def testar_slug_url_resolve_tenant():

    Empresa.objects.create(
        nome="Demo",
        documento="1",
        slug="demo",
        banco="iron_demo",
    )

    middleware = TenantMiddleware(lambda resposta: None)

    requisicao = RequisicaoFalsa("/demo/")

    middleware.process_request(requisicao)

    assert requisicao.tenant is not None
    assert requisicao.tenant.slug == "demo"
    assert requisicao.session["tenant_atual"] == "demo"


@pytest.mark.django_db
def testar_header_resolve_tenant():

    Empresa.objects.create(
        nome="Demo",
        documento="1",
        slug="demo",
        banco="iron_demo",
    )

    middleware = TenantMiddleware(lambda resposta: None)

    requisicao = RequisicaoFalsa(
        "/api/produtos/",
        {"X-Tenant": "demo"},
    )

    middleware.process_request(requisicao)

    assert requisicao.tenant.slug == "demo"


@pytest.mark.django_db
def testar_sessao_resolve_tenant():

    Empresa.objects.create(
        nome="Demo",
        documento="1",
        slug="demo",
        banco="iron_demo",
    )

    middleware = TenantMiddleware(lambda resposta: None)

    requisicao = RequisicaoFalsa("/admin/")
    requisicao.session["tenant_atual"] = "demo"

    middleware.process_request(requisicao)

    assert requisicao.tenant.slug == "demo"


@pytest.mark.django_db
def testar_slug_reservado_nao_resolve():

    middleware = TenantMiddleware(lambda resposta: None)

    requisicao = RequisicaoFalsa("/admin/")

    middleware.process_request(requisicao)

    assert requisicao.tenant is None
