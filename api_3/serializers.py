from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import RelatedField
from carmaker.models import VehicleModel, Project, Manufacturer


class ProjectCodeNameField(RelatedField):
    queryset = Project.objects.all()

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return getattr(value, "code_name")


class ManufacturerNameField(RelatedField):
    queryset = Manufacturer.objects.all()

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return getattr(value, "name")


class VehicleModelSerializer(ModelSerializer):
    maker = ManufacturerNameField()
    project_code_name = ProjectCodeNameField(source="project")

    def to_internal_value(self, data):
        new_data = super().to_internal_value(data)
        new_data["maker"] = Manufacturer.objects.get(name=new_data["maker"])
        return new_data

    def create(self, validated_data):
        if validated_data.get("project"):
            validated_data["project"] = Project.objects.create(code_name=validated_data["project"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        project_name = validated_data.pop("project", None)
        if project_name is not None and instance.project.code_name != project_name:
            instance.project.delete()
            validated_data["project"] = Project.objects.create(code_name=project_name)
        return super().update(instance, validated_data)

    class Meta:
        model = VehicleModel
        fields = "__all__"
