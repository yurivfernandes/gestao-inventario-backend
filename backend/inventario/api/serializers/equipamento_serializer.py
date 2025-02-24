from rest_framework import serializers

from ...models import Equipamento


class EquipamentoSerializer(serializers.ModelSerializer):
    site_codigo_vivo = serializers.CharField(
        source="site.codigo_vivo", read_only=True
    )

    class Meta:
        model = Equipamento
        fields = [
            "id",
            "site",
            "tipo",
            "status",
            "fornecedor",
            "modelo",
            "serial_number",
            "redundancia",
            "hw_end_life_cycle",
            "hw_end_support",
            "sw_end_life_cycle",
            "sw_end_support",
            "site_codigo_vivo",
        ]
