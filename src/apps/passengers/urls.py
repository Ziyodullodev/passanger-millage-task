from django.urls import path

from .views import PassengerMileageView

urlpatterns = [
    path("passengers/mileage/", PassengerMileageView.as_view(), name="passenger-milaege"),
]
