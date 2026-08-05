from django.core.management.base import BaseCommand

from apps.tenants.models import Empresa
from apps.tenants.services.provisionamento import ProvisionamentoService


class Command(BaseCommand):
    help = "Aplica migrações pendentes em todos os bancos dos tenants."

    def handle(self, *args, **options):

        empresas = Empresa.objects.filter(ativo=True)

        for empresa in empresas:

            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    f"Migrando {empresa.nome} ({empresa.banco})..."
                )
            )

            ProvisionamentoService.executar_migracoes_tenant(empresa.banco)

        self.stdout.write(
            self.style.SUCCESS(
                f"{empresas.count()} tenant(s) migrado(s)."
            )
        )
