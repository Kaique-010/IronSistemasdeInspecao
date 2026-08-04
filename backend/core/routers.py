from core.tenant_context import get_current_tenant


class TenantRouter:


    def db_for_read(self, model, **hints):

        tenant = get_current_tenant()

        if tenant:
            return tenant.banco

        return "default"



    def db_for_write(self, model, **hints):

        tenant = get_current_tenant()

        if tenant:
            return tenant.banco

        return "default"



    def allow_relation(self, obj1, obj2, **hints):

        return True



    def allow_migrate(self, db, app_label, model_name=None, **hints):

        return True