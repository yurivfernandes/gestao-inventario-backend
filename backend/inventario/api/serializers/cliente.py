from rest_framework import serializers

from ...models import Cliente, GrupoEconomico
from .grupo_economico import GrupoEconomicoSerializer


class ClienteSerializer(serializers.ModelSerializer):
    grupo_economico_detail = GrupoEconomicoSerializer(
        source="grupo_economico", read_only=True
    )
    grupo_economico = serializers.PrimaryKeyRelatedField(
        queryset=GrupoEconomico.objects.all(), required=False
    )

    class Meta:
        model = Cliente
        fields = [
            "id",
            "vantive_id",
            "razao_social",
            "codigo",
            "status",
            "status_vantive",
            "cnpj",
            "grupo_economico",
            "grupo_economico_detail",
        ]
