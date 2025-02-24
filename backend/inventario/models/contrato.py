from django.db import models


class Contrato(models.Model):
    equipamento = models.ForeignKey("Equipamento", on_delete=models.CASCADE)
    sku = models.CharField(max_length=100)
    data_registro = models.DateField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "d_contrato"
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"

    def __str__(self):
        return f"{self.sku}"
