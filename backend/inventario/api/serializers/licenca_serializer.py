from rest_framework import serializers

from ...models import Contrato, Licenca


class LicencaSerializer(serializers.ModelSerializer):
    contrato = serializers.PrimaryKeyRelatedField(
        queryset=Contrato.objects.all(), required=False
    )

    class Meta:
        model = Licenca
        fields = "__all__"
