from rest_framework.serializers import ModelSerializer

from carmaker.models import VehicleModel, Project, Manufacturer, Engine, Vehicle, Engineer


class ManufacturerSerializer(ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"


class EngineSerializer(ModelSerializer):
    class Meta:
        model = Engine
        fields = "__all__"


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class VehicleSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class EngineerSerializer(ModelSerializer):
    class Meta:
        model = Engineer
        fields = "__all__"


class VehicleModelSerializer(ModelSerializer):
    project = ProjectSerializer()
    maker = ManufacturerSerializer()
    engine_options = EngineSerializer(many=True)
    vehicle_set = VehicleSerializer(many=True)
    engineers_responsible = EngineerSerializer(many=True, source="engineer_set.all")

    class Meta:
        model = VehicleModel
        fields = "__all__"
