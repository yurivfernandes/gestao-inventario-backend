from rest_framework import serializers

from ...models import Equipamento, Site


class EquipamentoSerializer(serializers.ModelSerializer):
    site = serializers.PrimaryKeyRelatedField(
        queryset=Site.objects.all(), required=False
    )

    class Meta:
        model = Equipamento
        fields = "__all__"

    def update(self, instance, validated_data):
        # Remove site se presente nos dados validados
        validated_data.pop("site", None)
        return super().update(instance, validated_data)
