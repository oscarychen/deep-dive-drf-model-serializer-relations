from django.urls import path, include

urlpatterns = [
    path("api_1/", include("api_1.urls")),
    path("api_2/", include("api_2.urls"))
]
