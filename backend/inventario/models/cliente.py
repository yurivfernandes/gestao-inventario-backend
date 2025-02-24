from django.db import models

from .grupo_economico import GrupoEconomico


class Cliente(models.Model):
    vantive_id = models.CharField(max_length=50)
    razao_social = models.CharField(max_length=255)
    codigo = models.CharField(max_length=30)
    status = models.BooleanField()
    cnpj = models.CharField(max_length=14, unique=True)
    grupo_economico = models.ForeignKey(
        GrupoEconomico, on_delete=models.PROTECT, null=False
    )
    status_vantive = models.CharField(max_length=50)

    class Meta:
        db_table = "d_cliente"
