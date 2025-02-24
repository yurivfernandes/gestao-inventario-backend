from rest_framework import serializers

from ...models import GrupoEconomico


class GrupoEconomicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoEconomico
        fields = [
            "id",
            "vantive_id",
            "razao_social",
            "codigo",
            "status",
            "cnpj",
        ]
