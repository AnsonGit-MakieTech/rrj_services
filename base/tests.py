from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch


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

    def test_admin_toggle_renders_admin_navigation_variant(self):
        with patch("base.views.IS_ADMIN", True):
            response = self.client.get(reverse("home"))

        self.assertContains(response, "site-header-admin")
        self.assertContains(response, "Admin")
        self.assertContains(response, "Settings")

    def test_customer_navigation_hides_admin_items(self):
        with patch("base.views.IS_ADMIN", False):
            response = self.client.get(reverse("home"))

        self.assertNotContains(response, "site-header-admin")
        self.assertNotContains(response, 'aria-label="Admin dashboard"')
        self.assertNotContains(response, 'aria-label="Admin settings"')


class AuthenticationPageTests(TestCase):
    def test_login_page_uses_name_and_contact_number_fields(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login to your account")
        self.assertContains(response, 'name="full_name"')
        self.assertContains(response, 'name="contact_number"')
        self.assertNotContains(response, 'type="password"')
        self.assertContains(response, reverse("register"))

    def test_register_page_uses_name_and_contact_number_fields(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create an account")
        self.assertContains(response, 'name="full_name"')
        self.assertContains(response, 'name="contact_number"')
        self.assertNotContains(response, 'type="password"')
        self.assertContains(response, reverse("login"))
        self.assertContains(response, "assets/rrj-logo.png")


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
        self.assertContains(response, "Pending Quotation")
        self.assertContains(response, "BK-MPL5LPV3")
        self.assertContains(response, reverse("view_booking", args=["BK-MPL5LPV3"]))


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


class ViewBookingPageTests(TestCase):
    def test_detail_page_renders_simulated_workflow_state(self):
        response = self.client.get(reverse("view_booking", args=["BK-MPL5LPV3"]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BK-MPL5LPV3")
        self.assertContains(response, "Carpentry")
        self.assertContains(response, "Pending Quotation")
        self.assertContains(response, "Progress")
        self.assertContains(response, "Messages")

    def test_quotation_sent_simulation_displays_decision_actions(self):
        with patch("base.views.SIMULATED_VIEW_BOOKING_STATUS", "quotation_sent"):
            response = self.client.get(reverse("view_booking", args=["BK-MPL5LPV3"]))

        self.assertContains(response, "Quotation Sent")
        self.assertContains(response, "Accept")
        self.assertContains(response, "Reject")

    def test_waiting_payment_simulation_displays_payment_form(self):
        with patch("base.views.SIMULATED_VIEW_BOOKING_STATUS", "waiting_for_payment"):
            response = self.client.get(reverse("view_booking", args=["BK-MPL5LPV3"]))

        self.assertContains(response, "Waiting for Payment")
        self.assertContains(response, "Upload Payment Proof")
        self.assertContains(response, "data-payment-select")
        self.assertContains(response, "data-receipt-input")
        self.assertContains(response, 'type="file" name="receipt"')
        self.assertContains(response, "Submit Payment")
