from ..models import Empresa, MembroEmpresa


def empresas_do_usuario(usuario):

    if usuario.is_superuser:
        return Empresa.objects.filter(ativo=True)

    ids = MembroEmpresa.objects.filter(
        usuario=usuario,
        ativo=True,
        empresa__ativo=True,
    ).values_list('empresa_id', flat=True)

    return Empresa.objects.filter(id__in=ids)


def usuario_tem_acesso(usuario, empresa):

    if not usuario or not usuario.is_authenticated:
        return False

    if usuario.is_superuser:
        return True

    return MembroEmpresa.objects.filter(
        usuario=usuario,
        empresa=empresa,
        ativo=True,
    ).exists()


def papéis_do_usuario(usuario):

    papeis = {}

    for membro in MembroEmpresa.objects.filter(
        usuario=usuario,
        ativo=True,
    ).select_related('empresa'):
        papeis[membro.empresa.slug] = membro.papel

    return papeis
