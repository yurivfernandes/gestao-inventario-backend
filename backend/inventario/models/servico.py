from django.db import models

from .equipamento import Equipamento


class Servico(models.Model):
    equipamento = models.OneToOneField(Equipamento, on_delete=models.CASCADE)
    servico_num = models.CharField(max_length=50)
    oferta = models.CharField(max_length=100)
    pacote = models.CharField(max_length=100)
    redundancia = models.BooleanField(default=False)
    operadora = models.CharField(max_length=100)
    ip = models.CharField(max_length=50)
    ra = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "d_servico"
