from apps.tenants.services.acesso import empresas_do_usuario


def tenant(request):

    contexto = {
        "tenant_atual": getattr(request, "tenant", None),
        "empresas_usuario": [],
    }

    if request.user.is_authenticated:
        contexto["empresas_usuario"] = empresas_do_usuario(request.user)

    return contexto
