from django.core.management.base import BaseCommand

from apps.tenants.services.tenant_services import TenantService


class Command(BaseCommand):

    help = "Cria um novo tenant"


    def add_arguments(self, parser):

        parser.add_argument(
            "--nome",
            required=True
        )

        parser.add_argument(
            "--documento",
            required=True
        )


    def handle(self, *args, **options):

        empresa = TenantService.criar_empresa(
            nome=options["nome"],
            documento=options["documento"],
        )


        self.stdout.write(
            self.style.SUCCESS(
                f"""
Tenant criado com sucesso!

Empresa:
{empresa.nome}

Banco:
{empresa.banco}
"""
            )
        )