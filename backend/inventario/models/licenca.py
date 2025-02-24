from django.db import models


class Licenca(models.Model):
    contrato = models.ForeignKey("Contrato", on_delete=models.CASCADE)
    licenca_numero = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.licenca_numero

    class Meta:
        db_table = "d_licenca"
        verbose_name = "Licença"
        verbose_name_plural = "Licenças"
