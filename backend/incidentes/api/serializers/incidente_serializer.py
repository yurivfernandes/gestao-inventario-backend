from incidentes.models import Incidente
from rest_framework import serializers


class IncidenteSerializer(serializers.ModelSerializer):
    data_abertura = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    data_fechamento = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False
    )
    data_resolucao = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False
    )

    class Meta:
        model = Incidente
        fields = "__all__"
