from django.db import models

from .cliente import Cliente


class Site(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    razao_social = models.CharField(max_length=255)
    cep = models.CharField(max_length=10)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    codigo_sys_cliente = models.CharField(max_length=30)
    codigo_vivo = models.CharField(max_length=30)
    status = models.BooleanField()
    tipo_site = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=14)

    class Meta:
        db_table = "d_site"
