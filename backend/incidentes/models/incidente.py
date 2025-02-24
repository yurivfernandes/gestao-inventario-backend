from django.db import models


class Incidente(models.Model):
    aberto_por = models.CharField(max_length=50)
    categoria = models.CharField(max_length=100)
    codigo_equipamento = models.CharField(max_length=50)
    codigo_servico = models.CharField(max_length=50)
    data_abertura = models.DateTimeField()
    data_fechamento = models.DateTimeField(null=True, blank=True)
    data_resolucao = models.DateTimeField(null=True, blank=True)
    duracao = models.DurationField()
    descricao = models.TextField()
    fila = models.CharField(max_length=50)
    incidente = models.CharField(max_length=50)
    origem = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    subcategoria = models.CharField(max_length=100)
    subcategoria_detalhe = models.CharField(max_length=200)
    tipo_contato = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "f_incidente"

    def __str__(self):
        return f"Incidente {self.incidente} - {self.status}"
