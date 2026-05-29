import shutil
import tempfile
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from base.models import BookingRequest, Service


class AuthenticatedPageTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="639123456789",
            password=None,
            full_name="Makie Tech",
            contact_number="639123456789",
        )
        self.client.force_login(self.user)

    def make_user_staff(self):
        self.user.is_staff = True
        self.user.save(update_fields=["is_staff"])
        self.client.force_login(self.user)

    def create_booking_request(
        self,
        reference="BK-TEST0001",
        owner=None,
        service_name="Wall Repair",
        full_name="Customer One",
        progress="pending_quotation",
        amount_paid=0,
        material_cost=0,
        labor_cost=0,
        total_cost=0,
    ):
        if owner is None:
            owner = self.user
        service = Service.objects.create(name=service_name)
        return BookingRequest.objects.create(
            owner=owner,
            service=service,
            reference_number=reference,
            full_name=full_name,
            email="customer@example.com",
            contact_number="09123456789",
            full_address="Manila",
            project_location="Makati",
            square_meters=24,
            urgency_level="high",
            service_description="Service scope",
            problem_description="Project notes",
            progress=progress,
            amount_paid=amount_paid,
            material_cost=material_cost,
            labor_cost=labor_cost,
            total_cost=total_cost,
            transaction_notes="Admin quotation notes",
        )


class HomePageTests(AuthenticatedPageTestCase):
    def test_home_page_renders_customer_dashboard_content(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Build Better.")
        self.assertContains(response, "Condo Renovation")
        self.assertContains(response, "RRJ's Maintenance Services")
        self.assertContains(response, "assets/rrj-logo-icon")
        self.assertContains(response, "images.unsplash.com")
        self.assertContains(response, 'alt="Condo Renovation"')

    def test_staff_user_renders_admin_navigation_variant(self):
        self.make_user_staff()
        response = self.client.get(reverse("home"))

        self.assertContains(response, "site-header-admin")
        self.assertContains(response, "Admin")
        self.assertContains(response, "Settings")
        self.assertContains(response, reverse("admin_dashboard"))
        self.assertContains(response, reverse("service_settings"))

    def test_customer_navigation_hides_admin_items(self):
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
        self.assertContains(response, "assets/rrj-logo")


class AuthenticationApiTests(TestCase):
    def test_register_api_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("api_register"),
            {
                "full_name": "Juan Dela Cruz",
                "contact_number": "0912 345 6789",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["redirect_url"], reverse("home"))
        self.assertIn("_auth_user_id", self.client.session)

        User = get_user_model()
        self.assertTrue(
            User.objects.filter(
                full_name="Juan Dela Cruz",
                contact_number="639123456789",
            ).exists()
        )

    def test_login_api_logs_in_registered_user(self):
        User = get_user_model()
        User.objects.create_user(
            username="639123456789",
            password=None,
            full_name="Makie Tech",
            contact_number="639123456789",
        )

        response = self.client.post(
            reverse("api_login"),
            {
                "full_name": "makie tech",
                "contact_number": "09123456789",
                "next": reverse("services"),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["redirect_url"], reverse("services"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_api_rejects_unknown_user(self):
        response = self.client.post(
            reverse("api_login"),
            {
                "full_name": "Unknown User",
                "contact_number": "09123456789",
            },
        )

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("_auth_user_id", self.client.session)


class PageProtectionTests(TestCase):
    def test_home_requires_login(self):
        response = self.client.get(reverse("home"))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('home')}")


class AdminDashboardPageTests(AuthenticatedPageTestCase):
    def test_admin_dashboard_renders_metrics_charts_and_bookings_for_staff(self):
        self.make_user_staff()
        User = get_user_model()
        customer = User.objects.create_user(
            username="639555000001",
            password=None,
            full_name="Maria Customer",
            contact_number="639555000001",
        )
        self.create_booking_request(
            reference="BK-REAL0001",
            owner=customer,
            service_name="Kitchen Renovation",
            full_name="Maria Customer",
            progress="pending_quotation",
        )
        self.create_booking_request(
            reference="BK-REAL0002",
            owner=customer,
            service_name="Roof Repair",
            full_name="Maria Customer",
            progress="completed",
            amount_paid=5000,
        )

        response = self.client.get(reverse("admin_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Dashboard")
        self.assertContains(response, "Total Bookings")
        self.assertContains(response, "Active Jobs")
        self.assertContains(response, "PHP 5,000")
        self.assertContains(response, "Monthly Bookings")
        self.assertContains(response, "Most Requested Services")
        self.assertContains(response, "data-admin-monthly-chart")
        self.assertContains(response, "data-admin-service-chart")
        self.assertContains(response, "admin-monthly-chart-data")
        self.assertContains(response, "chart.js@4.5.0")
        self.assertContains(response, "BK-REAL0001")
        self.assertContains(response, "Maria Customer")
        self.assertContains(response, "Kitchen Renovation")
        self.assertContains(response, "data-admin-search")
        self.assertContains(response, "data-admin-status-select")
        self.assertContains(response, "Quotation Sent")
        self.assertContains(response, "Payment Verification")
        self.assertContains(response, "In Progress")
        self.assertContains(response, "js/admin.")
        self.assertContains(response, "site-header-admin")
        self.assertContains(response, f'class="active" href="{reverse("admin_dashboard")}"')
        self.assertContains(response, reverse("admin_view_booking", args=["BK-REAL0001"]))

    def test_admin_dashboard_empty_state_uses_real_booking_table(self):
        self.make_user_staff()

        response = self.client.get(reverse("admin_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No booking requests received yet.")
        self.assertContains(response, "PHP 0")

    def test_admin_dashboard_is_not_available_for_customer(self):
        response = self.client.get(reverse("admin_dashboard"))

        self.assertEqual(response.status_code, 404)


class AdminViewBookingPageTests(AuthenticatedPageTestCase):
    def test_confirmed_booking_renders_admin_controls_for_staff(self):
        self.make_user_staff()
        self.create_booking_request(
            reference="BK-ADMIN001",
            service_name="Shower Enclosure Install",
            full_name="Erijerehua Guaguitin",
            progress="booking_confirmed",
        )
        response = self.client.get(reverse("admin_view_booking", args=["BK-ADMIN001"]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Shower Enclosure Install")
        self.assertContains(response, "Erijerehua Guaguitin")
        self.assertContains(response, "Booking Confirmed")
        self.assertContains(response, "Update Status")
        self.assertContains(response, "Scheduled")
        self.assertContains(response, "Messages")
        self.assertContains(response, "Progress")
        self.assertContains(response, f'class="active" href="{reverse("admin_dashboard")}"')

    def test_pending_quotation_simulation_displays_quotation_form(self):
        self.make_user_staff()
        self.create_booking_request(reference="BK-ADMIN002", progress="pending_quotation")
        response = self.client.get(reverse("admin_view_booking", args=["BK-ADMIN002"]))

        self.assertContains(response, "Pending Quotation")
        self.assertContains(response, "Send Quotation")
        self.assertContains(response, "Materials Cost")
        self.assertContains(response, 'type="number" name="materials_cost"')
        self.assertContains(response, 'type="number" name="labor_cost"')
        self.assertContains(response, 'type="number" name="total_amount"')
        self.assertNotContains(response, 'aria-label="Payment verification"')

    def test_payment_verification_simulation_displays_review_actions(self):
        self.make_user_staff()
        self.create_booking_request(
            reference="BK-ADMIN003",
            progress="payment_verification",
            amount_paid=1200,
            total_cost=1200,
        )
        response = self.client.get(reverse("admin_view_booking", args=["BK-ADMIN003"]))

        self.assertContains(response, "Payment Verification")
        self.assertContains(response, "Approve Payment")
        self.assertContains(response, "Reject Payment")
        self.assertContains(response, "PHP 1,200")

    def test_scheduled_simulation_only_displays_remaining_status_actions(self):
        self.make_user_staff()
        self.create_booking_request(reference="BK-ADMIN004", progress="scheduled")
        response = self.client.get(reverse("admin_view_booking", args=["BK-ADMIN004"]))

        self.assertContains(response, "Update Status")
        self.assertContains(response, "In Progress")
        self.assertContains(response, "Completed")
        self.assertNotContains(response, '<button type="button">Scheduled</button>')

    def test_in_progress_simulation_only_displays_completed_action(self):
        self.make_user_staff()
        self.create_booking_request(reference="BK-ADMIN005", progress="in_progress")
        response = self.client.get(reverse("admin_view_booking", args=["BK-ADMIN005"]))

        self.assertContains(response, "Update Status")
        self.assertContains(response, '<button type="button">Completed</button>')
        self.assertNotContains(response, '<button type="button">Scheduled</button>')
        self.assertNotContains(response, '<button type="button">In Progress</button>')

    def test_existing_completed_dashboard_booking_keeps_its_status(self):
        self.make_user_staff()
        self.create_booking_request(reference="BK-ADMIN006", progress="completed")
        response = self.client.get(reverse("admin_view_booking", args=["BK-ADMIN006"]))

        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Update Status")

    def test_admin_booking_page_is_not_available_for_customer(self):
        self.create_booking_request(reference="BK-ADMIN007")
        response = self.client.get(reverse("admin_view_booking", args=["BK-ADMIN007"]))

        self.assertEqual(response.status_code, 404)


class ServiceSettingsPageTests(AuthenticatedPageTestCase):
    def test_settings_page_renders_service_management_and_modals_for_staff(self):
        self.make_user_staff()
        response = self.client.get(reverse("service_settings"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Service Settings")
        self.assertContains(response, "Manage service categories and pricing.")
        self.assertContains(response, "Baseboard Maker")
        self.assertContains(response, "data-settings-search")
        self.assertContains(response, "data-service-modal=\"add\"")
        self.assertContains(response, "Add New Service")
        self.assertContains(response, "Edit Service")
        self.assertContains(response, "Cover Photo", count=2)
        self.assertContains(response, 'name="image"', count=2)
        self.assertContains(response, 'name="status"', count=2)
        self.assertContains(response, "data-service-status-select", count=2)
        self.assertContains(response, "Taking new bookings", count=6)
        self.assertContains(response, "data-service-delete-modal")
        self.assertContains(response, "Keep Service")
        self.assertNotContains(response, "confirm('Delete this service?')")
        self.assertContains(response, "data-service-cover-preview", count=2)
        self.assertContains(response, "site-header-admin")
        self.assertContains(response, f'class="active" href="{reverse("service_settings")}"')

    def test_settings_page_is_not_available_for_customer(self):
        response = self.client.get(reverse("service_settings"))

        self.assertEqual(response.status_code, 404)


class ManageServiceApiTests(AuthenticatedPageTestCase):
    def test_staff_can_create_service(self):
        self.make_user_staff()

        response = self.client.post(
            reverse("create_service"),
            {
                "name": "Solar Panel Cleaning",
                "description": "Panel cleaning and inspection.",
                "min_price": "2500",
                "max_price": "12000",
                "status": "available",
                "is_active": "1",
            },
        )

        self.assertRedirects(response, reverse("service_settings"))
        service = Service.objects.get(name="Solar Panel Cleaning")
        self.assertEqual(service.description, "Panel cleaning and inspection.")
        self.assertEqual(service.min_price, 2500)
        self.assertEqual(service.max_price, 12000)
        self.assertEqual(service.status, "available")
        self.assertTrue(service.is_active)
        self.assertFalse(service.is_deleted)

    def test_staff_can_update_toggle_and_delete_service(self):
        self.make_user_staff()
        service = Service.objects.create(
            name="Old Service",
            description="Old description",
            min_price=100,
            max_price=500,
            is_active=True,
            status="available",
        )

        response = self.client.post(
            reverse("update_service"),
            {
                "service_id": service.id,
                "name": "Updated Service",
                "description": "Updated description",
                "min_price": "300",
                "max_price": "900",
                "status": "fully_booked",
                "is_active": "1",
            },
        )
        self.assertRedirects(response, reverse("service_settings"))

        service.refresh_from_db()
        self.assertEqual(service.name, "Updated Service")
        self.assertEqual(service.status, "fully_booked")
        self.assertEqual(service.min_price, 300)
        self.assertEqual(service.max_price, 900)

        response = self.client.post(
            reverse("toggle_service_status", args=[service.id]),
            {"is_active": "0"},
        )
        self.assertRedirects(response, reverse("service_settings"))
        service.refresh_from_db()
        self.assertFalse(service.is_active)

        response = self.client.post(reverse("delete_service", args=[service.id]))
        self.assertRedirects(response, reverse("service_settings"))
        service.refresh_from_db()
        self.assertTrue(service.is_deleted)
        self.assertFalse(service.is_active)

    def test_customer_cannot_manage_services(self):
        service = Service.objects.create(name="Customer Blocked Service")

        response = self.client.post(reverse("delete_service", args=[service.id]))

        self.assertEqual(response.status_code, 404)
        service.refresh_from_db()
        self.assertFalse(service.is_deleted)


class ServicesPageTests(AuthenticatedPageTestCase):
    def test_services_page_renders_full_catalog(self):
        response = self.client.get(reverse("services"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search services...")
        self.assertContains(response, "Baseboard Maker")
        self.assertContains(response, "Condo Renovation")
        self.assertContains(response, "Carpentry")
        self.assertContains(response, "images.unsplash.com")


class MyBookingsPageTests(AuthenticatedPageTestCase):
    def test_my_bookings_page_renders_dashboard_fixture_data(self):
        response = self.client.get(reverse("my_bookings"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Bookings")
        self.assertContains(response, "New Booking")
        self.assertContains(response, "Pending Quotation")
        self.assertContains(response, "BK-MPL5LPV3")
        self.assertContains(response, reverse("view_booking", args=["BK-MPL5LPV3"]))


class AddBookingPageTests(AuthenticatedPageTestCase):
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
        self.assertContains(response, 'data-booking-form')
        self.assertContains(response, reverse("create_booking"))
        self.assertContains(response, 'name="attachments"')
        self.assertContains(response, "data-booking-confirmation-modal")
        self.assertContains(response, "js/add_booking.")
        self.assertContains(response, "data-booking-select")
        self.assertContains(response, "data-booking-date-field")
        self.assertContains(response, "Optional target visit day")
        self.assertContains(response, "Condo Renovation")
        self.assertNotContains(response, '<select name="service_id"')


class ManageBookingApiTests(AuthenticatedPageTestCase):
    def setUp(self):
        super().setUp()
        self.media_root = tempfile.mkdtemp()
        self.media_override = self.settings(MEDIA_ROOT=self.media_root)
        self.media_override.enable()
        self.addCleanup(self.media_override.disable)
        self.addCleanup(shutil.rmtree, self.media_root, ignore_errors=True)

    def test_customer_can_create_booking_with_multiple_images(self):
        service = Service.objects.create(
            name="Wall Repair",
            is_active=True,
            status="available",
        )
        image_one = SimpleUploadedFile(
            "before.png",
            b"image-one",
            content_type="image/png",
        )
        image_two = SimpleUploadedFile(
            "angle.jpg",
            b"image-two",
            content_type="image/jpeg",
        )

        response = self.client.post(
            reverse("create_booking"),
            {
                "full_name": "Makie Tech",
                "email": "techmakie@gmail.com",
                "contact_number": "09123456789",
                "full_address": "Manila",
                "service_id": str(service.id),
                "urgency_level": "high",
                "preferred_date": "2026-06-01",
                "square_meters": "24.5",
                "project_location": "Kitchen wall",
                "service_description": "Repair and repaint",
                "problem_description": "Cracked wall",
                "attachments": [image_one, image_two],
            },
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertTrue(payload["success"])
        self.assertTrue(payload["reference_number"].startswith("BK-"))
        self.assertEqual(payload["redirect_url"], reverse("view_booking", args=[payload["reference_number"]]))

        booking = BookingRequest.objects.get(reference_number=payload["reference_number"])
        self.assertEqual(booking.owner, self.user)
        self.assertEqual(booking.service, service)
        self.assertEqual(booking.urgency_level, "high")
        self.assertEqual(booking.attachments.count(), 2)

    def test_booking_api_rejects_non_image_attachment(self):
        service = Service.objects.create(
            name="Painting",
            is_active=True,
            status="available",
        )
        attachment = SimpleUploadedFile(
            "scope.pdf",
            b"not-an-image",
            content_type="application/pdf",
        )

        response = self.client.post(
            reverse("create_booking"),
            {
                "full_name": "Makie Tech",
                "email": "techmakie@gmail.com",
                "service_id": str(service.id),
                "attachments": [attachment],
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        self.assertEqual(BookingRequest.objects.count(), 0)


class ViewBookingPageTests(AuthenticatedPageTestCase):
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
