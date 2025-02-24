from rest_framework import serializers

from ...models import Contrato, Equipamento


class ContratoSerializer(serializers.ModelSerializer):
    equipamento = serializers.PrimaryKeyRelatedField(
        queryset=Equipamento.objects.all(), required=False
    )

    class Meta:
        model = Contrato
        fields = "__all__"
