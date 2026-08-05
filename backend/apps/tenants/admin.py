from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Empresa, MembroEmpresa
from .services.tenant_services import TenantService


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "slug",
        "banco",
        "ativo",
        "data_cadastro",
    )
    list_filter = (
        "ativo",
        "data_cadastro",
    )
    search_fields = (
        "nome",
        "slug",
        "documento",
    )

    def save_model(self, request, obj, form, change):

        if not change:

            empresa = TenantService.criar_empresa(
                nome=obj.nome,
                documento=obj.documento,
                endereco=obj.endereco,
                telefone=obj.telefone,
                email=obj.email,
            )

            obj.id = empresa.id

        else:
            super().save_model(
                request,
                obj,
                form,
                change
            )


@admin.register(MembroEmpresa)
class MembroEmpresaAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "empresa",
        "papel",
        "ativo",
        "data_cadastro",
    )
    list_filter = (
        "empresa",
        "papel",
        "ativo",
    )
    search_fields = (
        "usuario__username",
        "usuario__email",
        "empresa__nome",
        "empresa__slug",
    )
    autocomplete_fields = (
        "usuario",
        "empresa",
    )
