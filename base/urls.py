from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("services/", views.services, name="services"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("my-bookings/<str:reference>/", views.view_booking, name="view_booking"),
    path("add-booking/", views.add_booking, name="add_booking"),
]
