from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from api_2.serializers import VehicleModelSerializer
from carmaker.models import VehicleModel


class VehicleModelListCreateView(ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer


class VehicleModelRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer
