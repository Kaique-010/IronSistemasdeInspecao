from django.contrib import admin
from .models import Empresa
from .services.tenant_services import TenantService



@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "slug",
        "banco",
        "ativo",
           )
    list_filter = (
        "nome",
        "slug",
        "ativo",

    )
    search_fields = (
        "nome",
        "slug",

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
