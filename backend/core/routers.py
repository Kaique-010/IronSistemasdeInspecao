from core.tenant_context import obter_tenant_atual
from core.tenant_utils import registrar_banco_tenant


class TenantRouter:


    def db_for_read(self, model, **hints):

        tenant = obter_tenant_atual()

        if tenant:
            return registrar_banco_tenant(
                tenant.banco
            )

        return "default"



    def db_for_write(self, model, **hints):

        tenant = obter_tenant_atual()

        if tenant:
            return registrar_banco_tenant(
                tenant.banco
            )

        return "default"



    def allow_relation(self, obj1, obj2, **hints):

        return True



    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if db.startswith("iron_"):
            return True

        return True