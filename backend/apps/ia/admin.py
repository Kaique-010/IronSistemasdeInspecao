from django.contrib import admin

from apps.ia.models import ModeloIA


@admin.register(ModeloIA)
class ModeloIAAdmin(admin.ModelAdmin):

    list_display = ['nome', 'tipo', 'versao', 'ativo']
    list_filter = ['tipo', 'ativo']
    search_fields = ['nome', 'versao']
