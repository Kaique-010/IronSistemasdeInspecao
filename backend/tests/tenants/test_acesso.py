import pytest

from django.contrib.auth import get_user_model

from apps.tenants.models import Empresa, MembroEmpresa
from apps.tenants.services.acesso import empresas_do_usuario, usuario_tem_acesso


@pytest.mark.django_db
def testar_membro_tem_acesso_apenas_sua_empresa():

    usuario = get_user_model().objects.create_user(
        username="operador",
        password="x",
    )

    empresa_a = Empresa.objects.create(
        nome="A",
        documento="1",
        slug="a",
        banco="iron_a",
    )

    empresa_b = Empresa.objects.create(
        nome="B",
        documento="1",
        slug="b",
        banco="iron_b",
    )

    MembroEmpresa.objects.create(
        usuario=usuario,
        empresa=empresa_a,
        papel=MembroEmpresa.Papel.OPERADOR,
    )

    assert usuario_tem_acesso(usuario, empresa_a)
    assert not usuario_tem_acesso(usuario, empresa_b)

    assert list(
        empresas_do_usuario(usuario).values_list("slug", flat=True)
    ) == ["a"]


@pytest.mark.django_db
def testar_superuser_acessa_todas_empresas():

    usuario = get_user_model().objects.create_user(
        username="admin",
        password="x",
        is_superuser=True,
    )

    empresa_a = Empresa.objects.create(
        nome="A",
        documento="1",
        slug="a",
        banco="iron_a",
    )

    empresa_b = Empresa.objects.create(
        nome="B",
        documento="1",
        slug="b",
        banco="iron_b",
    )

    assert usuario_tem_acesso(usuario, empresa_a)
    assert usuario_tem_acesso(usuario, empresa_b)
    assert empresas_do_usuario(usuario).count() == 2


@pytest.mark.django_db
def testar_sem_usuario_sem_acesso():

    empresa = Empresa.objects.create(
        nome="A",
        documento="1",
        slug="a",
        banco="iron_a",
    )

    assert not usuario_tem_acesso(None, empresa)
