from django.utils.deprecation import MiddlewareMixin

from .models import Empresa
from core.tenant_context import setar_tenant_atual

SEGMENTOS_RESERVADOS = {
    "admin",
    "api",
    "tenant",
    "static",
    "media",
    "docs",
    "health",
}


class TenantMiddleware(MiddlewareMixin):

    def process_request(self, request):

        empresa = self._resolver_tenant(request)

        request.tenant = empresa

        if empresa:
            setar_tenant_atual(empresa)

    def process_response(self, request, response):

        setar_tenant_atual(None)

        return response

    def _resolver_tenant(self, request):

        empresa = self._resolver_por_slug_url(request)

        if empresa:
            return empresa

        empresa = self._resolver_por_header(request)

        if empresa:
            return empresa

        return self._resolver_por_sessao(request)

    def _resolver_por_slug_url(self, request):

        caminho = request.path_info.strip("/")

        if not caminho:
            return None

        primeiro = caminho.split("/")[0]

        if not primeiro or primeiro in SEGMENTOS_RESERVADOS:
            return None

        empresa = self._buscar_por_slug(primeiro)

        if empresa and hasattr(request, "session"):
            if request.session.get("tenant_atual") != empresa.slug:
                request.session["tenant_atual"] = empresa.slug

        return empresa

    def _resolver_por_header(self, request):

        slug = request.headers.get("X-Tenant")

        if not slug:
            return None

        return self._buscar_por_slug(slug)

    def _resolver_por_sessao(self, request):

        if not hasattr(request, "session"):
            return None

        slug = request.session.get("tenant_atual")

        if not slug:
            return None

        return self._buscar_por_slug(slug)

    def _buscar_por_slug(self, slug):

        try:
            return Empresa.objects.get(slug=slug, ativo=True)
        except Empresa.DoesNotExist:
            return None
