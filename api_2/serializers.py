from rest_framework.serializers import ModelSerializer
from django.db.models import Q
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
        fields = ("id", "name",)


class VehicleModelSerializer(ModelSerializer):
    project = ProjectSerializer()
    maker = ManufacturerSerializer()
    engine_options = EngineSerializer(many=True)
    vehicle_set = VehicleSerializer(many=True, read_only=True)
    engineers_responsible = EngineerSerializer(many=True, source="engineer_set")

    def to_internal_value(self, data):

        new_data = super().to_internal_value(data)

        new_data["maker"] = Manufacturer.objects.get(**new_data["maker"])

        engine_options_q = Q()
        for engine in new_data["engine_options"]:
            engine_options_q |= Q(**engine)
        new_data["engine_options"] = Engine.objects.filter(engine_options_q)

        engineer_set_q = Q()
        for engineer in new_data["engineer_set"]:
            engineer_set_q |= Q(**engineer)
        new_data["engineer_set"] = Engineer.objects.filter(engineer_set_q)

        return new_data

    def update(self, instance, validated_data):
        project_data = validated_data.pop("project", None)
        if project_data and instance.project.code_name != project_data["code_name"]:
            instance.project.delete()
            validated_data["project"] = Project.objects.create(**project_data)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        validated_data["project"] = Project.objects.create(**validated_data.pop("project"))
        instance = super().create(validated_data)
        return instance

    class Meta:
        model = VehicleModel
        fields = "__all__"
