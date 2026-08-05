from django.conf import settings
from django.db import models
from django.utils.text import slugify



class Empresa(models.Model):
    nome = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    documento = models.CharField(max_length=18)

    endereco = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    telefone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    email = models.EmailField(
        max_length=255,
        blank=True,
        null=True
    )

    banco = models.CharField(
        max_length=255,
        unique=True,
        editable=False
    )

    ativo = models.BooleanField(default=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)


    def gerar_nome_banco(self):
        return f"iron_{self.slug}"


    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.nome)

        if not self.banco:
            self.banco = f"iron_{self.slug.replace('-', '_')}"

        super().save(*args, **kwargs)


class MembroEmpresa(models.Model):

    class Papel(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        OPERADOR = 'operador', 'Operador'
        VISUALIZADOR = 'visualizador', 'Visualizador'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='membros',
        verbose_name='Usuário',
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='membros',
        verbose_name='Empresa',
    )

    papel = models.CharField(
        max_length=20,
        choices=Papel.choices,
        default=Papel.OPERADOR,
        verbose_name='Papel',
    )

    ativo = models.BooleanField(default=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Membro da Empresa'
        verbose_name_plural = 'Membros das Empresas'
        unique_together = ('usuario', 'empresa')

    def __str__(self):
        return f'{self.usuario} - {self.empresa.nome} ({self.get_papel_display()})'