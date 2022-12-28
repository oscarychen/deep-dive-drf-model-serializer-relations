from rest_framework.serializers import ModelSerializer

from carmaker.models import VehicleModel


class VehicleModelSerializer(ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = "__all__"
