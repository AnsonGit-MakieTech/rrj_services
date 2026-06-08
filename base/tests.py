import shutil
import tempfile
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from base.models import BookingRequest, ChatMessage, Service, SystemSettings


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

    def test_home_page_uses_system_settings_when_available(self):
        SystemSettings.objects.create(
            tagline="Reliable repairs for busy property owners",
            description="Book maintenance, review quotations, and track work from one place.",
        )

        response = self.client.get(reverse("home"))

        self.assertContains(response, "Reliable repairs for busy property owners")
        self.assertContains(response, "Book maintenance, review quotations, and track work from one place.")
        self.assertNotContains(response, "Build Better.")

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
        self.assertContains(response, "data-uppercase-name")
        self.assertContains(response, 'autocapitalize="characters"')
        self.assertContains(response, 'name="contact_number"')
        self.assertNotContains(response, 'type="password"')
        self.assertContains(response, reverse("register"))

    def test_register_page_uses_name_and_contact_number_fields(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create an account")
        self.assertContains(response, 'name="full_name"')
        self.assertContains(response, "data-uppercase-name")
        self.assertContains(response, 'autocapitalize="characters"')
        self.assertContains(response, 'name="contact_number"')
        self.assertNotContains(response, 'type="password"')
        self.assertContains(response, reverse("login"))
        self.assertContains(response, "assets/rrj-logo")


class ErrorPageTests(AuthenticatedPageTestCase):
    @override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
    def test_unknown_url_renders_custom_404_for_authenticated_user(self):
        response = self.client.get("/missing-page/")

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Page not found", status_code=404)
        self.assertContains(response, "RRJ's Maintenance Services", status_code=404)
        self.assertContains(response, reverse("home"), status_code=404)
        self.assertContains(response, reverse("my_bookings"), status_code=404)

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
    def test_unknown_url_renders_custom_404_for_guest(self):
        self.client.logout()

        response = self.client.get("/missing-page/")

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Page not found", status_code=404)
        self.assertContains(response, reverse("login"), status_code=404)
        self.assertContains(response, reverse("register"), status_code=404)


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
                full_name="JUAN DELA CRUZ",
                first_name="JUAN",
                last_name="DELA CRUZ",
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
        self.assertContains(response, reverse("update_booking_status", args=["BK-ADMIN001"]))
        self.assertContains(response, 'name="progress" value="scheduled"')
        self.assertNotContains(response, 'name="progress" value="in_progress"')
        self.assertNotContains(response, 'name="progress" value="completed"')
        self.assertContains(response, f'class="active" href="{reverse("admin_dashboard")}"')

    def test_pending_quotation_simulation_displays_quotation_form(self):
        self.make_user_staff()
        self.create_booking_request(reference="BK-ADMIN002", progress="pending_quotation")
        response = self.client.get(reverse("admin_view_booking", args=["BK-ADMIN002"]))

        self.assertContains(response, "Pending Quotation")
        self.assertContains(response, "Send Quotation")
        self.assertContains(response, "Materials Cost")
        self.assertContains(response, reverse("submit_booking_quotation", args=["BK-ADMIN002"]))
        self.assertContains(response, "data-booking-transaction-form")
        self.assertContains(response, "js/booking_transactions.")
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
        self.assertContains(response, reverse("verify_booking_payment", args=["BK-ADMIN003"]))
        self.assertContains(response, "data-booking-transaction-form")

    def test_scheduled_simulation_only_displays_remaining_status_actions(self):
        self.make_user_staff()
        self.create_booking_request(reference="BK-ADMIN004", progress="scheduled")
        response = self.client.get(reverse("admin_view_booking", args=["BK-ADMIN004"]))

        self.assertContains(response, "Update Status")
        self.assertContains(response, 'name="progress" value="in_progress"')
        self.assertContains(response, 'name="progress" value="completed"')
        self.assertNotContains(response, '<button type="button">Scheduled</button>')
        self.assertNotContains(response, 'name="progress" value="scheduled"')

    def test_in_progress_simulation_displays_reschedule_and_completed_actions(self):
        self.make_user_staff()
        self.create_booking_request(reference="BK-ADMIN005", progress="in_progress")
        response = self.client.get(reverse("admin_view_booking", args=["BK-ADMIN005"]))

        self.assertContains(response, "Update Status")
        self.assertContains(response, 'name="progress" value="scheduled"')
        self.assertContains(response, 'name="progress" value="completed"')
        self.assertNotContains(response, '<button type="button">Scheduled</button>')
        self.assertNotContains(response, '<button type="button">In Progress</button>')
        self.assertNotContains(response, 'name="progress" value="in_progress"')

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
        self.assertContains(response, "Manage homepage content, service categories, and pricing.")
        self.assertContains(response, "Homepage Content")
        self.assertContains(response, "data-system-settings-open")
        self.assertContains(response, "data-system-settings-modal")
        self.assertContains(response, "data-system-settings-close")
        self.assertContains(response, reverse("update_system_settings"))
        self.assertContains(response, 'name="tagline"')
        self.assertContains(response, 'name="description"')
        self.assertContains(response, "Blank fields use the default homepage copy.")
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


class ManageSystemSettingsApiTests(AuthenticatedPageTestCase):
    def test_staff_can_update_homepage_content(self):
        self.make_user_staff()

        response = self.client.post(
            reverse("update_system_settings"),
            {
                "tagline": "Reliable repairs for every property",
                "description": "Request work, approve quotations, and track progress online.",
            },
        )

        self.assertRedirects(response, reverse("service_settings"))
        settings = SystemSettings.objects.latest("pk")
        self.assertEqual(settings.tagline, "Reliable repairs for every property")
        self.assertEqual(settings.description, "Request work, approve quotations, and track progress online.")

        response = self.client.get(reverse("home"))
        self.assertContains(response, "Reliable repairs for every property")
        self.assertContains(response, "Request work, approve quotations, and track progress online.")

    def test_staff_can_reset_homepage_content_to_defaults(self):
        self.make_user_staff()
        SystemSettings.objects.create(
            tagline="Old custom copy",
            description="Old custom description.",
        )

        response = self.client.post(
            reverse("update_system_settings"),
            {
                "tagline": "",
                "description": "",
            },
        )

        self.assertRedirects(response, reverse("service_settings"))
        settings = SystemSettings.objects.latest("pk")
        self.assertEqual(settings.tagline, "")
        self.assertEqual(settings.description, "")

        response = self.client.get(reverse("home"))
        self.assertContains(response, "Build Better.")
        self.assertContains(response, "Professional construction and maintenance services at your fingertips.")

    def test_customer_cannot_update_homepage_content(self):
        response = self.client.post(
            reverse("update_system_settings"),
            {
                "tagline": "Blocked",
                "description": "Blocked",
            },
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(SystemSettings.objects.exists())


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
    def test_customer_my_bookings_page_renders_only_owned_bookings(self):
        User = get_user_model()
        other_user = User.objects.create_user(
            username="639555000002",
            password=None,
            full_name="Other Customer",
            contact_number="639555000002",
        )
        self.create_booking_request(
            reference="BK-MINE0001",
            service_name="Tiles Sitter",
            full_name="Makie Tech",
            progress="pending_quotation",
        )
        self.create_booking_request(
            reference="BK-OTHER001",
            owner=other_user,
            service_name="Roof Repair",
            full_name="Other Customer",
            progress="completed",
        )

        response = self.client.get(reverse("my_bookings"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Bookings")
        self.assertContains(response, "New Booking")
        self.assertContains(response, "Track your service requests and project progress.")
        self.assertContains(response, "Pending Quotation")
        self.assertContains(response, "BK-MINE0001")
        self.assertContains(response, "Tiles Sitter")
        self.assertContains(response, "data-my-booking-search")
        self.assertContains(response, "data-my-booking-status-select")
        self.assertContains(response, "js/my_booking.")
        self.assertContains(response, reverse("view_booking", args=["BK-MINE0001"]))
        self.assertNotContains(response, "BK-OTHER001")

    def test_admin_my_bookings_page_renders_all_received_bookings(self):
        self.make_user_staff()
        User = get_user_model()
        customer = User.objects.create_user(
            username="639555000003",
            password=None,
            full_name="Maria Customer",
            contact_number="639555000003",
        )
        self.create_booking_request(
            reference="BK-ADMINALL1",
            owner=customer,
            service_name="Condo Renovation",
            full_name="Maria Customer",
            progress="completed",
        )

        response = self.client.get(reverse("my_bookings"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "All Bookings")
        self.assertContains(response, "Review every customer request received")
        self.assertContains(response, "New Booking")
        self.assertContains(response, "BK-ADMINALL1")
        self.assertContains(response, "Maria Customer")
        self.assertContains(response, "Completed")
        self.assertContains(response, f'href="{reverse("add_booking")}"')
        self.assertContains(response, reverse("admin_view_booking", args=["BK-ADMINALL1"]))

    def test_my_bookings_page_renders_empty_state(self):
        response = self.client.get(reverse("my_bookings"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No bookings yet")
        self.assertContains(response, "Book a service to start a quotation request.")


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
        cache.clear()
        self.addCleanup(cache.clear)
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

    @override_settings(
        BOOKING_RATE_LIMIT_REQUESTS=3,
        BOOKING_RATE_LIMIT_WINDOW_SECONDS=3600,
    )
    def test_booking_api_rate_limits_fourth_request(self):
        service = Service.objects.create(
            name="Electrical Repair",
            is_active=True,
            status="available",
        )
        payload = {
            "full_name": "Makie Tech",
            "email": "techmakie@gmail.com",
            "service_id": str(service.id),
        }

        for _ in range(3):
            response = self.client.post(reverse("create_booking"), payload)
            self.assertEqual(response.status_code, 201)

        response = self.client.post(reverse("create_booking"), payload)

        self.assertEqual(response.status_code, 429)
        self.assertFalse(response.json()["success"])
        self.assertEqual(response["Retry-After"], "3600")
        self.assertEqual(response["X-RateLimit-Limit"], "3")
        self.assertEqual(response["X-RateLimit-Remaining"], "0")
        self.assertEqual(BookingRequest.objects.count(), 3)


class ViewBookingPageTests(AuthenticatedPageTestCase):
    def test_detail_page_renders_database_workflow_state(self):
        self.create_booking_request(
            reference="BK-DETAIL001",
            service_name="Carpentry",
            progress="pending_quotation",
        )

        response = self.client.get(reverse("view_booking", args=["BK-DETAIL001"]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BK-DETAIL001")
        self.assertContains(response, "Carpentry")
        self.assertContains(response, "Pending Quotation")
        self.assertContains(
            response,
            "Our customer service team will contact you soon via call or message.",
        )
        self.assertContains(response, "Progress")
        self.assertContains(response, "Messages")

    def test_quotation_sent_booking_displays_decision_actions(self):
        self.create_booking_request(
            reference="BK-DETAIL002",
            progress="quotation_sent",
            total_cost=4000,
        )

        response = self.client.get(reverse("view_booking", args=["BK-DETAIL002"]))

        self.assertContains(response, "Quotation Sent")
        self.assertContains(response, "Accept")
        self.assertContains(response, "Reject")
        self.assertContains(response, reverse("decide_booking_quotation", args=["BK-DETAIL002"]))
        self.assertContains(response, "data-booking-transaction-form")
        self.assertContains(response, "js/booking_transactions.")

    def test_waiting_payment_booking_displays_payment_form(self):
        self.create_booking_request(
            reference="BK-DETAIL003",
            progress="waiting_for_payment",
            total_cost=4000,
        )

        response = self.client.get(reverse("view_booking", args=["BK-DETAIL003"]))

        self.assertContains(response, "Waiting for Payment")
        self.assertContains(response, "Upload Payment Proof")
        self.assertContains(response, "data-payment-select")
        self.assertContains(response, "data-receipt-input")
        self.assertContains(response, 'type="file" name="receipt"')
        self.assertContains(response, 'name="payment_reference_number"')
        self.assertContains(response, reverse("submit_booking_payment", args=["BK-DETAIL003"]))
        self.assertContains(response, "data-booking-transaction-form")
        self.assertContains(response, "Submit Payment")

    def test_detail_page_404s_when_booking_is_missing(self):
        response = self.client.get(reverse("view_booking", args=["BK-MISSING"]))

        self.assertEqual(response.status_code, 404)


class BookingMessagingTests(AuthenticatedPageTestCase):
    def test_customer_can_view_and_send_booking_messages(self):
        User = get_user_model()
        admin_user = User.objects.create_user(
            username="639555000010",
            password=None,
            full_name="RRJ Staff",
            contact_number="639555000010",
            is_staff=True,
        )
        booking = self.create_booking_request(reference="BK-CHAT001")
        ChatMessage.objects.create(
            booking_request=booking,
            sender=admin_user,
            receiver=self.user,
            message="We are reviewing your request.",
        )

        response = self.client.get(reverse("view_booking", args=["BK-CHAT001"]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "We are reviewing your request.")
        self.assertContains(response, "RRJ Admin")
        self.assertContains(response, "data-booking-message-form")
        self.assertContains(response, reverse("booking_messages", args=["BK-CHAT001"]))
        self.assertContains(response, "js/booking_messaging.")

        response = self.client.post(
            reverse("booking_messages", args=["BK-CHAT001"]),
            {"message": "Thank you. Please send the quotation."},
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertTrue(payload["success"])
        self.assertTrue(payload["message"]["is_own"])

        chat_message = ChatMessage.objects.latest("id")
        self.assertEqual(chat_message.booking_request, booking)
        self.assertEqual(chat_message.sender, self.user)
        self.assertEqual(chat_message.receiver, admin_user)
        self.assertEqual(chat_message.message, "Thank you. Please send the quotation.")

    def test_admin_can_view_and_send_booking_messages(self):
        self.make_user_staff()
        User = get_user_model()
        customer = User.objects.create_user(
            username="639555000011",
            password=None,
            full_name="Maria Customer",
            contact_number="639555000011",
        )
        booking = self.create_booking_request(
            reference="BK-CHAT002",
            owner=customer,
            full_name="Maria Customer",
        )
        ChatMessage.objects.create(
            booking_request=booking,
            sender=customer,
            receiver=self.user,
            message="Can you check my uploaded files?",
        )

        response = self.client.get(reverse("admin_view_booking", args=["BK-CHAT002"]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Can you check my uploaded files?")
        self.assertContains(response, "Maria Customer")
        self.assertContains(response, "data-booking-message-form")
        self.assertContains(response, reverse("booking_messages", args=["BK-CHAT002"]))

        response = self.client.post(
            reverse("booking_messages", args=["BK-CHAT002"]),
            {"message": "Files received. We will prepare the quote."},
        )

        self.assertEqual(response.status_code, 201)
        chat_message = ChatMessage.objects.latest("id")
        self.assertEqual(chat_message.booking_request, booking)
        self.assertEqual(chat_message.sender, self.user)
        self.assertEqual(chat_message.receiver, customer)
        self.assertEqual(chat_message.message, "Files received. We will prepare the quote.")

    def test_customer_cannot_view_or_send_messages_for_other_customer_booking(self):
        User = get_user_model()
        other_user = User.objects.create_user(
            username="639555000012",
            password=None,
            full_name="Other Customer",
            contact_number="639555000012",
        )
        self.create_booking_request(reference="BK-CHAT003", owner=other_user)

        response = self.client.get(reverse("booking_messages", args=["BK-CHAT003"]))
        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            reverse("booking_messages", args=["BK-CHAT003"]),
            {"message": "Trying to access another booking."},
        )
        self.assertEqual(response.status_code, 404)


class BookingTransactionTests(AuthenticatedPageTestCase):
    def setUp(self):
        super().setUp()
        self.media_root = tempfile.mkdtemp()
        self.media_override = self.settings(MEDIA_ROOT=self.media_root)
        self.media_override.enable()
        self.addCleanup(self.media_override.disable)
        self.addCleanup(shutil.rmtree, self.media_root, ignore_errors=True)

    def test_admin_can_submit_quotation_and_notify_customer(self):
        self.make_user_staff()
        User = get_user_model()
        customer = User.objects.create_user(
            username="639555000013",
            password=None,
            full_name="Maria Customer",
            contact_number="639555000013",
        )
        booking = self.create_booking_request(
            reference="BK-QUOTE001",
            owner=customer,
            service_name="Kitchen Renovation",
            progress="pending_quotation",
            material_cost=0,
            labor_cost=0,
            total_cost=0,
        )

        response = self.client.post(
            reverse("submit_booking_quotation", args=["BK-QUOTE001"]),
            {
                "materials_cost": "2500",
                "labor_cost": "6500",
                "total_amount": "9000",
                "notes": "Includes materials and labor.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        booking.refresh_from_db()
        self.assertEqual(booking.progress, "quotation_sent")
        self.assertEqual(booking.material_cost, 2500)
        self.assertEqual(booking.labor_cost, 6500)
        self.assertEqual(booking.total_cost, 9000)
        self.assertEqual(booking.transaction_notes, "Includes materials and labor.")

        message = ChatMessage.objects.latest("id")
        self.assertEqual(message.booking_request, booking)
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.receiver, customer)
        self.assertIn("Quotation sent", message.message)
        self.assertIn("PHP 9,000", message.message)

    def test_customer_can_accept_quotation_and_move_to_payment(self):
        User = get_user_model()
        admin_user = User.objects.create_user(
            username="639555000014",
            password=None,
            full_name="RRJ Staff",
            contact_number="639555000014",
            is_staff=True,
        )
        booking = self.create_booking_request(
            reference="BK-QUOTE002",
            progress="quotation_sent",
            material_cost=1500,
            labor_cost=2500,
            total_cost=4000,
        )

        response = self.client.post(
            reverse("decide_booking_quotation", args=["BK-QUOTE002"]),
            {"decision": "accept"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        booking.refresh_from_db()
        self.assertEqual(booking.progress, "waiting_for_payment")

        message = ChatMessage.objects.latest("id")
        self.assertEqual(message.booking_request, booking)
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.receiver, admin_user)
        self.assertEqual(message.message, "Quotation accepted. Waiting for payment proof.")

    def test_customer_can_reject_quotation_for_revision(self):
        User = get_user_model()
        admin_user = User.objects.create_user(
            username="639555000015",
            password=None,
            full_name="RRJ Staff",
            contact_number="639555000015",
            is_staff=True,
        )
        booking = self.create_booking_request(
            reference="BK-QUOTE003",
            progress="quotation_sent",
            total_cost=4000,
        )

        response = self.client.post(
            reverse("decide_booking_quotation", args=["BK-QUOTE003"]),
            {"decision": "reject"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        booking.refresh_from_db()
        self.assertEqual(booking.progress, "pending_quotation")

        message = ChatMessage.objects.latest("id")
        self.assertEqual(message.booking_request, booking)
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.receiver, admin_user)
        self.assertEqual(message.message, "Quotation rejected. Please review and send an updated quotation.")

    def test_customer_cannot_decide_other_customer_quotation(self):
        User = get_user_model()
        other_user = User.objects.create_user(
            username="639555000016",
            password=None,
            full_name="Other Customer",
            contact_number="639555000016",
        )
        self.create_booking_request(
            reference="BK-QUOTE004",
            owner=other_user,
            progress="quotation_sent",
            total_cost=4000,
        )

        response = self.client.post(
            reverse("decide_booking_quotation", args=["BK-QUOTE004"]),
            {"decision": "accept"},
        )

        self.assertEqual(response.status_code, 404)

    def test_customer_can_submit_payment_proof_for_admin_verification(self):
        User = get_user_model()
        admin_user = User.objects.create_user(
            username="639555000017",
            password=None,
            full_name="RRJ Staff",
            contact_number="639555000017",
            is_staff=True,
        )
        booking = self.create_booking_request(
            reference="BK-PAY001",
            progress="waiting_for_payment",
            total_cost=4000,
        )
        receipt = SimpleUploadedFile(
            "receipt.png",
            b"receipt-image",
            content_type="image/png",
        )

        response = self.client.post(
            reverse("submit_booking_payment", args=["BK-PAY001"]),
            {
                "amount_paid": "4000",
                "payment_method": "g-cash",
                "payment_reference_number": "GCASH-123",
                "receipt": receipt,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        booking.refresh_from_db()
        self.assertEqual(booking.progress, "payment_verification")
        self.assertEqual(booking.amount_paid, 4000)
        self.assertEqual(booking.payment_method, "g-cash")
        self.assertEqual(booking.payment_reference_number, "GCASH-123")
        self.assertFalse(booking.approved_payment)
        self.assertTrue(booking.receipt_screenshot.name.startswith("receipts/"))

        message = ChatMessage.objects.latest("id")
        self.assertEqual(message.booking_request, booking)
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.receiver, admin_user)
        self.assertIn("Payment proof submitted", message.message)

    def test_admin_can_approve_payment_and_confirm_booking(self):
        self.make_user_staff()
        booking = self.create_booking_request(
            reference="BK-PAY002",
            progress="payment_verification",
            amount_paid=4000,
            total_cost=4000,
        )

        response = self.client.post(
            reverse("verify_booking_payment", args=["BK-PAY002"]),
            {"decision": "approve"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        booking.refresh_from_db()
        self.assertEqual(booking.progress, "booking_confirmed")
        self.assertTrue(booking.approved_payment)

        message = ChatMessage.objects.latest("id")
        self.assertEqual(message.booking_request, booking)
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.receiver, booking.owner)
        self.assertEqual(message.message, "Payment approved. Booking confirmed.")

    def test_admin_can_reject_payment_and_request_new_receipt(self):
        self.make_user_staff()
        booking = self.create_booking_request(
            reference="BK-PAY003",
            progress="payment_verification",
            amount_paid=4000,
            total_cost=4000,
        )
        booking.approved_payment = True
        booking.save(update_fields=["approved_payment"])

        response = self.client.post(
            reverse("verify_booking_payment", args=["BK-PAY003"]),
            {"decision": "reject"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        booking.refresh_from_db()
        self.assertEqual(booking.progress, "waiting_for_payment")
        self.assertFalse(booking.approved_payment)

        message = ChatMessage.objects.latest("id")
        self.assertEqual(message.booking_request, booking)
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.receiver, booking.owner)
        self.assertEqual(message.message, "Payment proof rejected. Please upload a new receipt for verification.")

    def test_admin_can_update_operational_status_and_customer_sees_it(self):
        self.make_user_staff()
        User = get_user_model()
        customer = User.objects.create_user(
            username="639555000018",
            password=None,
            full_name="Maria Customer",
            contact_number="639555000018",
        )
        booking = self.create_booking_request(
            reference="BK-STATUS001",
            owner=customer,
            progress="booking_confirmed",
        )

        response = self.client.post(
            reverse("update_booking_status", args=["BK-STATUS001"]),
            {"progress": "scheduled"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        booking.refresh_from_db()
        self.assertEqual(booking.progress, "scheduled")

        message = ChatMessage.objects.latest("id")
        self.assertEqual(message.booking_request, booking)
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.receiver, customer)
        self.assertEqual(message.message, "Booking scheduled. RRJ Admin updated the project status to Scheduled.")

        self.client.force_login(customer)
        response = self.client.get(reverse("view_booking", args=["BK-STATUS001"]))
        self.assertContains(response, "Scheduled")
        self.assertContains(response, "phase-current")

    def test_admin_cannot_use_invalid_status_transition(self):
        self.make_user_staff()
        booking = self.create_booking_request(
            reference="BK-STATUS002",
            progress="pending_quotation",
        )

        response = self.client.post(
            reverse("update_booking_status", args=["BK-STATUS002"]),
            {"progress": "completed"},
        )

        self.assertEqual(response.status_code, 400)
        booking.refresh_from_db()
        self.assertEqual(booking.progress, "pending_quotation")

    def test_admin_can_move_in_progress_back_to_scheduled_for_reschedule(self):
        self.make_user_staff()
        booking = self.create_booking_request(
            reference="BK-STATUS003",
            progress="in_progress",
        )

        response = self.client.post(
            reverse("update_booking_status", args=["BK-STATUS003"]),
            {"progress": "scheduled"},
        )

        self.assertEqual(response.status_code, 200)
        booking.refresh_from_db()
        self.assertEqual(booking.progress, "scheduled")

    def test_customer_cannot_update_booking_status(self):
        self.create_booking_request(
            reference="BK-STATUS004",
            progress="booking_confirmed",
        )

        response = self.client.post(
            reverse("update_booking_status", args=["BK-STATUS004"]),
            {"progress": "scheduled"},
        )

        self.assertEqual(response.status_code, 404)
