from django.db import connection
from django.utils.text import slugify

from .models import Empresa


class TenantService:

    @staticmethod
    def criar_empresa(
        nome,
        documento,
        endereco=None,
        telefone=None,
        email=None
    ):

        slug = slugify(nome)

        banco = f"iron_{slug.replace('-', '_')}"

        empresa = Empresa.objects.create(
            nome=nome,
            documento=documento,
            endereco=endereco,
            telefone=telefone,
            email=email,
            slug=slug,
            banco=banco
        )

        TenantService.criar_database(banco)

        return empresa


    @staticmethod
    def criar_database(nome_banco):

        with connection.cursor() as cursor:

            cursor.execute(
                f'CREATE DATABASE "{nome_banco}"'
            )