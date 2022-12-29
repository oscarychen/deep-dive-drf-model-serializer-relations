from . import views
from django.urls import path

urlpatterns = [
    path("", views.VehicleModelListCreateView.as_view()),
    path("<pk>/", views.VehicleModelRetrieveUpdateDestroyView.as_view())
]
