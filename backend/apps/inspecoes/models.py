from django.db import models


class Inspecao(models.Model):

    descricao = models.CharField(max_length=200)

    class Meta:
        app_label = "inspecoes"