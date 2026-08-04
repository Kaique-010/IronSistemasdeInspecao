from django.utils.deprecation import MiddlewareMixin

from .models import Empresa
from core.tenant_context import ( obter_tenant_atual, setar_tenant_atual

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

                setar_tenant_atual(empresa)

            except Empresa.DoesNotExist:
                request.tenant = None

        else:
            request.tenant = None


    def process_response(self, request, response):

        setar_tenant_atual(None)

        return response