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

        }

        connections.databases = settings.DATABASES