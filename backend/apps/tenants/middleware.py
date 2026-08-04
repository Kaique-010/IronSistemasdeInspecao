from django.utils.deprecation import MiddlewareMixin

from .models import Empresa
from core.tenant_context import (
    set_current_tenant,
    clear_current_tenant
)


class TenantMiddleware(MiddlewareMixin):

    def process_request(self, request):

        tenant_slug = request.headers.get("X-Tenant")

        if tenant_slug:

            try:
                empresa = Empresa.objects.get(
                    slug=tenant_slug,
                    ativo=True
                )

                request.tenant = empresa

                set_current_tenant(empresa)

            except Empresa.DoesNotExist:
                request.tenant = None

        else:
            request.tenant = None


    def process_response(self, request, response):

        clear_current_tenant()

        return response