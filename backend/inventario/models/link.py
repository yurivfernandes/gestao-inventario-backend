from django.db import models


class Link(models.Model):
    equipamento = models.ForeignKey("Equipamento", on_delete=models.CASCADE)
    operadora = models.CharField(max_length=100)
    designador = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.operadora} - {self.designador}"

    class Meta:
        db_table = "d_link"
        verbose_name = "Link"
        verbose_name_plural = "Links"
