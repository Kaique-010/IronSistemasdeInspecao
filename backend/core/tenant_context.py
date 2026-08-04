from threading import local


_thread_locals = local()


def setar_tenant_atual(tenant):
    _thread_locals.tenant = tenant


def obter_tenant_atual():
    return getattr(_thread_locals, "tenant", None)


def remover_tenant_atual_banco():
    if hasattr(_thread_locals, "tenant"):
        del _thread_locals.tenant.banco
