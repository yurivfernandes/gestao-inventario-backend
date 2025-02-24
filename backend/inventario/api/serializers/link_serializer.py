from rest_framework import serializers

from ...models import Equipamento, Link


class LinkSerializer(serializers.ModelSerializer):
    equipamento = serializers.PrimaryKeyRelatedField(
        queryset=Equipamento.objects.all(), required=False
    )

    class Meta:
        model = Link
        fields = "__all__"
