from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_page_renders_customer_dashboard_content(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Build Better.")
        self.assertContains(response, "Condo Renovation")
        self.assertContains(response, "RRJ's Maintenance Services")
        self.assertContains(response, "assets/rrj-logo-icon.png")
        self.assertContains(response, "images.unsplash.com")
        self.assertContains(response, 'alt="Condo Renovation"')


class ServicesPageTests(TestCase):
    def test_services_page_renders_full_catalog(self):
        response = self.client.get(reverse("services"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search services...")
        self.assertContains(response, "Condo Renovation")
        self.assertContains(response, "Carpentry")
        self.assertContains(response, "images.unsplash.com", count=16)


class MyBookingsPageTests(TestCase):
    def test_my_bookings_page_renders_dashboard_fixture_data(self):
        response = self.client.get(reverse("my_bookings"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Bookings")
        self.assertContains(response, "New Booking")
        self.assertContains(response, "Pending Quotation", count=2)
        self.assertContains(response, "BK-MPL5LPV3")


class AddBookingPageTests(TestCase):
    def test_add_booking_page_renders_ui_and_selected_service(self):
        response = self.client.get(
            reverse("add_booking"),
            {"service": "Condo Renovation"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Book a Service")
        self.assertContains(response, "Customer Information")
        self.assertContains(response, "Upload Project Files")
        self.assertContains(response, "data-attachment-list")
        self.assertContains(response, '<option value="Condo Renovation" selected>')
