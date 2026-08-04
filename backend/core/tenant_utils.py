from django.db import connections
from core.tenant_context import obter_tenant_atual
from django.conf import settings



def obter_banco_atual():

    tenant = obter_tenant_atual()

    if tenant:
        return tenant.banco

    return "default"



def obter_conexao_banco():

    banco = obter_banco_atual()

    return connections[banco]



def executar_no_tenant(sql, parametros=None):

    conexao = obter_conexao_banco()

    with conexao.cursor() as cursor:
        cursor.execute(
            sql,
            parametros or []
        )

        return cursor.fetchall()


def registrar_banco_tenant(nome_banco):

    if nome_banco not in settings.DATABASES:

        settings.DATABASES[nome_banco] = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": nome_banco,
            "USER": settings.DATABASES["default"]["USER"],
            "PASSWORD": settings.DATABASES["default"]["PASSWORD"],
            "HOST": settings.DATABASES["default"]["HOST"],
            "PORT": settings.DATABASES["default"]["PORT"],
            "OPTIONS": {},
            "ATOMIC_REQUESTS": False,
            "AUTOCOMMIT": True,
            "CONN_MAX_AGE": 0,
            "CONN_HEALTH_CHECKS": False,
            "TIME_ZONE": None,
        }

        connections.databases[nome_banco] = settings.DATABASES[nome_banco]


    return nome_banco