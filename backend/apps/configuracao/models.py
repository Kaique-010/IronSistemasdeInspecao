from django.db import models


class Linha(models.Model):

    nome = models.CharField(max_length=255)
    codigo = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Código',
    )

    descricao = models.TextField(blank=True)

    produto = models.ForeignKey(
        'produtos.Produto',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='linhas',
        verbose_name='Produto inspecionado',
    )

    ativo = models.BooleanField(default=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Linha'
        verbose_name_plural = 'Linhas'
        ordering = ['nome']

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


class Camera(models.Model):

    class TipoCamera(models.TextChoices):
        IP = 'ip', 'IP'
        USB = 'usb', 'USB'
        STREAM = 'stream', 'Stream'

    nome = models.CharField(max_length=255)
    identificador = models.CharField(
        max_length=255,
        verbose_name='Identificador (IP/URL)',
    )

    tipo = models.CharField(
        max_length=20,
        choices=TipoCamera.choices,
        default=TipoCamera.IP,
    )

    linha = models.ForeignKey(
        'configuracao.Linha',
        on_delete=models.PROTECT,
        related_name='cameras',
    )

    ativo = models.BooleanField(default=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Câmera'
        verbose_name_plural = 'Câmeras'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.identificador})'


class Workflow(models.Model):

    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)

    produto = models.ForeignKey(
        'produtos.Produto',
        on_delete=models.PROTECT,
        related_name='workflows',
    )

    ativo = models.BooleanField(default=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Workflow'
        verbose_name_plural = 'Workflows'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Etapa(models.Model):

    class TipoEtapa(models.TextChoices):
        DETECCAO = 'deteccao', 'Detecção'
        CLASSIFICACAO = 'classificacao', 'Classificação'
        DESTINO = 'destino', 'Destino'

    workflow = models.ForeignKey(
        'configuracao.Workflow',
        on_delete=models.CASCADE,
        related_name='etapas',
    )

    ordem = models.PositiveIntegerField()

    tipo = models.CharField(
        max_length=50,
        choices=TipoEtapa.choices,
    )

    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'
        ordering = ['ordem']
        unique_together = ('workflow', 'ordem')

    def __str__(self):
        return f'{self.workflow.nome} - {self.ordem}: {self.get_tipo_display()}'
