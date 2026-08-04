import pytest

from apps.tenants.models import Empresa
from core.tenant_context import setar_tenant_atual
from core.routers import TenantRouter


@pytest.mark.django_db
def testar_router_escrita():

    empresa = Empresa.objects.create(
        nome="Teste",
        documento="123",
        slug="teste",
        banco="iron_teste",
    )

    setar_tenant_atual(empresa)

    router = TenantRouter()

    assert router.db_for_write(Empresa) == "iron_teste"