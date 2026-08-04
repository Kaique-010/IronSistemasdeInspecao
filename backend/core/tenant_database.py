from django.conf import settings


def configurar_banco_tenant(tenant):

    nome = tenant.banco

    if nome not in settings.DATABASES:

        settings.DATABASES[nome] = {
            **settings.DATABASES["default"],
            "NAME": nome,
        }

    return nome