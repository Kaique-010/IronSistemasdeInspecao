from core.tenant_context import obter_tenant_atual
from core.tenant_utils import registrar_banco_tenant

APPS_PUBLICOS = {
    "admin",
    "auth",
    "contenttypes",
    "sessions",
    "messages",
    "tenants",
}


class TenantRouter:

    def _banco_para_modelo(self, model):

        app_label = model._meta.app_label

        if app_label in APPS_PUBLICOS:
            return "default"

        tenant = obter_tenant_atual()

        if tenant:
            return registrar_banco_tenant(tenant.banco)

        return "default"


    def db_for_read(self, model, **hints):
        return self._banco_para_modelo(model)


    def db_for_write(self, model, **hints):
        return self._banco_para_modelo(model)


    def allow_relation(self, obj1, obj2, **hints):
        return True


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
