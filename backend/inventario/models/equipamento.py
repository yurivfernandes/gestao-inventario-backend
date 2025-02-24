from django.db import models

from .site import Site


class Equipamento(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    status = models.BooleanField()
    fornecedor = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    redundancia = models.BooleanField(default=False)
    hw_end_life_cycle = models.DateField(null=True, blank=True)
    hw_end_support = models.DateField(null=True, blank=True)
    sw_end_life_cycle = models.DateField(null=True, blank=True)
    sw_end_support = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "d_equipamento"
