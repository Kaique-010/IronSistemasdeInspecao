from django.db import models


class Produto(models.Model):

    nome = models.CharField(max_length=255)
    codigo = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Código (SKU)',
    )

    descricao = models.TextField(blank=True)
    categoria = models.CharField(
        max_length=100,
        blank=True,
    )

    ativo = models.BooleanField(default=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        return f'{self.codigo} - {self.nome}'
