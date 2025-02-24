from rest_framework import serializers

from ...models import Cliente, Site


class SiteSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), required=False
    )

    class Meta:
        model = Site
        fields = "__all__"

    def update(self, instance, validated_data):
        # Remove cliente se presente nos dados validados
        validated_data.pop("cliente", None)
        return super().update(instance, validated_data)
