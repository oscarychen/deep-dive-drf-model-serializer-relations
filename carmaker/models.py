from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=64)


class Engine(models.Model):
    name = models.CharField(max_length=128)
    displacement = models.FloatField()


class Project(models.Model):
    code_name = models.CharField(max_length=128, unique=True)


class VehicleModel(models.Model):
    model = models.CharField(max_length=256)
    year = models.IntegerField()
    project = models.OneToOneField(Project, on_delete=models.SET_NULL, null=True)
    maker = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True)
    predecessor = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    engine_options = models.ManyToManyField(Engine)


class Vehicle(models.Model):
    VIN = models.CharField(max_length=18)
    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)


class Engineer(models.Model):
    name = models.CharField(max_length=128)
    works_on = models.ManyToManyField(VehicleModel)
