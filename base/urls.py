from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_page, name="logout"),
    path("api/login/", views.api_login, name="api_login"),
    path("api/register/", views.api_register, name="api_register"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/bookings/<str:reference>/", views.admin_view_booking, name="admin_view_booking"),
    path("settings/", views.service_settings, name="service_settings"),
    path("services/", views.services, name="services"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("my-bookings/<str:reference>/", views.view_booking, name="view_booking"),
    path("add-booking/", views.add_booking, name="add_booking"),
]
