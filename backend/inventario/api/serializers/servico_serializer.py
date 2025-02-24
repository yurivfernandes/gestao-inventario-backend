from rest_framework import serializers

from ...models import Equipamento, Servico


class ServicoSerializer(serializers.ModelSerializer):
    equipamento = serializers.PrimaryKeyRelatedField(
        queryset=Equipamento.objects.all(), required=False
    )
    equipamento_codigo = serializers.CharField(
        source="equipamento.modelo", read_only=True
    )
    site_codigo_vivo = serializers.CharField(
        source="equipamento.site.codigo_vivo", read_only=True
    )

    def validate_redundancia(self, value):
        if isinstance(value, str):
            return value.lower() == "true"
        return bool(value)

    class Meta:
        model = Servico
        fields = [
            "id",
            "equipamento",
            "designador",
            "servico_num",
            "oferta",
            "pacote",
            "redundancia",
            "operadora",
            "ip",
            "ra",
            "status",
            "equipamento_codigo",
            "site_codigo_vivo",
        ]
