from django.views.generic import TemplateView

from apps.tenants.services.acesso import empresas_do_usuario


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            ctx["empresas"] = empresas_do_usuario(self.request.user)
        else:
            ctx["empresas"] = []

        return ctx
