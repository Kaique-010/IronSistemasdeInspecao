from django.conf import settings
from django.db import connections


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
