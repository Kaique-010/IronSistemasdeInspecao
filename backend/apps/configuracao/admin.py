from django.contrib import admin

from apps.configuracao.models import Camera, Etapa, Linha, Workflow


class EtapaInline(admin.TabularInline):

    model = Etapa
    extra = 0


@admin.register(Linha)
class LinhaAdmin(admin.ModelAdmin):

    list_display = ['codigo', 'nome', 'produto', 'ativo']
    list_filter = ['ativo', 'produto']
    search_fields = ['nome', 'codigo']


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):

    list_display = ['nome', 'identificador', 'tipo', 'linha', 'ativo']
    list_filter = ['tipo', 'ativo', 'linha']
    search_fields = ['nome', 'identificador']


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):

    list_display = ['nome', 'produto', 'ativo']
    list_filter = ['ativo', 'produto']
    search_fields = ['nome']
    inlines = [EtapaInline]


@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):

    list_display = ['workflow', 'ordem', 'tipo', 'ativo']
    list_filter = ['tipo', 'ativo']
