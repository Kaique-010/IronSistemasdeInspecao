from django.db import models


class ModeloIA(models.Model):

    class TipoModelo(models.TextChoices):
        DETECTOR = 'detector', 'Detector'
        CLASSIFICADOR = 'classificador', 'Classificador'

    nome = models.CharField(max_length=255)
    tipo = models.CharField(
        max_length=50,
        choices=TipoModelo.choices,
        default=TipoModelo.DETECTOR,
    )

    versao = models.CharField(max_length=50)
    arquivo = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Caminho do peso',
    )

    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Modelo de IA'
        verbose_name_plural = 'Modelos de IA'
        ordering = ['nome']
        unique_together = ('nome', 'versao')

    def __str__(self):
        return f'{self.nome} v{self.versao}'
