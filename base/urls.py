from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("add-booking/", views.add_booking, name="add_booking"),
]
