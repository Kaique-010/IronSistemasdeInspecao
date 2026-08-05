from django.contrib import admin

from apps.produtos.models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):

    list_display = ['codigo', 'nome', 'categoria', 'ativo', 'data_cadastro']
    list_filter = ['ativo', 'categoria']
    search_fields = ['nome', 'codigo']
    ordering = ['nome']
