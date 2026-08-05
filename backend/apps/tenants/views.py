import shutil
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from apps.configuracao.models import Workflow
from apps.ia.models import ModeloIA
from apps.ia.services.deteccao import executar_deteccao, resolver_caminho_modelo
from apps.produtos.models import Produto

from .models import Empresa
from .services.acesso import empresas_do_usuario, usuario_tem_acesso


def tenant_test(request):

    if request.tenant:

        return JsonResponse({
            "empresa": request.tenant.nome,
            "banco": request.tenant.banco
        })

    return JsonResponse({
        "empresa": None
    })


@require_POST
def trocar_tenant(request):

    slug = request.POST.get("empresa")

    empresa = get_object_or_404(Empresa, slug=slug, ativo=True)

    if not usuario_tem_acesso(request.user, empresa):
        return JsonResponse({
            "erro": "Sem acesso a essa empresa.",
        }, status=403)

    request.session["tenant_atual"] = empresa.slug
    request.session["tenant_anterior"] = slug

    destino = request.POST.get("destino")

    if destino:
        return redirect(destino)

    return redirect("admin:index")


def minhas_empresas(request):

    if not request.user.is_authenticated:
        return JsonResponse({"empresas": []}, status=401)

    empresas = empresas_do_usuario(request.user)

    dados = [
        {
            "slug": e.slug,
            "nome": e.nome,
        }
        for e in empresas
    ]

    atual = None

    if request.tenant:
        atual = request.tenant.slug

    return JsonResponse({
        "atual": atual,
        "empresas": dados,
    })


class TenantHomeView(TemplateView):
    template_name = "core/tenant_home.html"

    def get(self, request, tenant_slug):

        empresa = get_object_or_404(
            Empresa,
            slug=tenant_slug,
            ativo=True,
        )

        if request.tenant != empresa:
            request.tenant = empresa

        return super().get(request, tenant_slug=tenant_slug)

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)

        ctx["tenant"] = self.request.tenant
        ctx["workflows"] = Workflow.objects.filter(ativo=True).select_related("produto")
        ctx["modelos"] = ModeloIA.objects.filter(ativo=True)
        ctx["quantidade_produtos"] = Produto.objects.count()
        ctx["quantidade_workflows"] = Workflow.objects.filter(ativo=True).count()

        return ctx


@require_POST
def detectar(request, tenant_slug):

    empresa = get_object_or_404(
        Empresa,
        slug=tenant_slug,
        ativo=True,
    )

    if request.tenant != empresa:
        request.tenant = empresa

    pasta = settings.MEDIA_ROOT / "detecoes" / empresa.slug
    pasta.mkdir(parents=True, exist_ok=True)

    sufixo = str(uuid.uuid4())[:8]
    entrada = pasta / f"{sufixo}_entrada.jpg"
    saida = pasta / f"{sufixo}_anotada.jpg"

    imagem = request.FILES.get("imagem")
    exemplo = request.POST.get("exemplo")

    if not imagem and not exemplo:
        return JsonResponse({
            "erro": "Envie uma imagem ou selecione um exemplo.",
        }, status=400)

    if exemplo:

        nome_seguro = exemplo.split("/")[-1].split("\\")[-1]

        caminho_exemplo = settings.IA_SAMPLES / nome_seguro

        if not caminho_exemplo.exists():
            return JsonResponse({
                "erro": f"Exemplo não encontrado: {nome_seguro}",
            }, status=400)

        shutil.copy2(caminho_exemplo, entrada)

    else:

        with open(entrada, "wb") as destino:
            for pedaco in imagem.chunks():
                destino.write(pedaco)

    modelo_id = request.POST.get("modelo")

    if modelo_id:
        modelo = get_object_or_404(ModeloIA, id=modelo_id, ativo=True)
        peso = modelo.arquivo or settings.IA_MODELO_PADRAO
        nome_modelo = str(modelo)
    else:
        primeiro = ModeloIA.objects.filter(ativo=True).first()

        if primeiro:
            peso = primeiro.arquivo or settings.IA_MODELO_PADRAO
            nome_modelo = str(primeiro)
        else:
            peso = settings.IA_MODELO_PADRAO
            nome_modelo = "Modelo padrão"

    peso = resolver_caminho_modelo(peso)

    resultado = executar_deteccao(
        entrada,
        peso,
        saida,
        conf=float(request.POST.get("conf", 0.30)),
    )

    resultado["entrada"] = _url_media(entrada)
    resultado["modelo_nome"] = nome_modelo

    if "erro" not in resultado:
        resultado["imagem"] = _url_media(saida)

    return JsonResponse(resultado)


def _url_media(caminho):

    relativo = caminho.relative_to(settings.MEDIA_ROOT)

    return f"{settings.MEDIA_URL}{relativo.as_posix()}"
