from django.core.management import call_command
from core.database import registrar_banco_tenant


class ProvisionamentoService:

    @staticmethod
    def executar_migracoes_tenant(nome_banco):

        registrar_banco_tenant(nome_banco)

        call_command(
            "migrate",
            database=nome_banco,
            interactive=False
        )