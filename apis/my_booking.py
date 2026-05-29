from django.urls import reverse
from django.utils import timezone

from base.models import BookingRequest


PENDING_PROGRESS = {"pending_quotation", "quotation_sent", "waiting_for_payment", "payment_verification"}
ACTIVE_PROGRESS = {"booking_confirmed", "scheduled", "in_progress"}
STATUS_KIND_BY_PROGRESS = {
    "pending_quotation": "pending",
    "quotation_sent": "pending",
    "waiting_for_payment": "payment",
    "payment_verification": "payment",
    "booking_confirmed": "active",
    "scheduled": "active",
    "in_progress": "active",
    "completed": "completed",
    "cancelled": "cancelled",
}


def get_my_booking_context(user):
    is_admin = user.is_staff
    bookings = _booking_queryset(user, is_admin)
    booking_rows = [_booking_row(booking, is_admin) for booking in bookings]

    return {
        "booking_page_title": "All Bookings" if is_admin else "My Bookings",
        "booking_page_description": (
            "Review every customer request received by RRJ's Maintenance Services."
            if is_admin
            else "Track your service requests and project progress."
        ),
        "booking_primary_action_label": "New Booking",
        "booking_primary_action_url": reverse("add_booking"),
        "booking_empty_title": "No booking requests yet" if is_admin else "No bookings yet",
        "booking_empty_message": (
            "New customer requests will appear here after they submit a booking."
            if is_admin
            else "Book a service to start a quotation request."
        ),
        "bookings": booking_rows,
        "booking_stats": _booking_stats(bookings),
        "booking_status_options": _status_options(),
    }


def _booking_queryset(user, is_admin):
    queryset = (
        BookingRequest.objects.select_related("owner", "service")
        .prefetch_related("attachments")
        .order_by("-created_at")
    )
    if not is_admin:
        queryset = queryset.filter(owner=user)
    return list(queryset)


def _booking_row(booking, is_admin):
    description = booking.problem_description or booking.service_description or ""
    customer = _customer_name(booking)
    return {
        "reference": booking.reference_number,
        "customer": customer,
        "service": booking.service.name,
        "status": booking.get_progress_display(),
        "status_kind": STATUS_KIND_BY_PROGRESS.get(booking.progress, "pending"),
        "date": _format_datetime(booking.created_at),
        "description": description,
        "detail_url": reverse(
            "admin_view_booking" if is_admin else "view_booking",
            args=[booking.reference_number],
        ),
        "search": " ".join(
            [
                booking.reference_number or "",
                customer,
                booking.service.name or "",
                booking.get_progress_display(),
                description,
            ]
        ),
    }


def _booking_stats(bookings):
    pending_count = _count_progress(bookings, PENDING_PROGRESS)
    active_count = _count_progress(bookings, ACTIVE_PROGRESS)
    completed_count = _count_progress(bookings, {"completed"})
    return [
        {"label": "Total", "value": str(len(bookings)), "kind": "total"},
        {"label": "Pending", "value": str(pending_count), "kind": "pending"},
        {"label": "Active", "value": str(active_count), "kind": "active"},
        {"label": "Completed", "value": str(completed_count), "kind": "completed"},
    ]


def _status_options():
    return [
        {"label": "All Statuses", "value": ""},
        *[
            {"label": label, "value": label}
            for _, label in BookingRequest._meta.get_field("progress").choices
        ],
    ]


def _customer_name(booking):
    owner_name = getattr(booking.owner, "full_name", "") or booking.owner.get_full_name() or booking.owner.username
    return booking.full_name or owner_name


def _count_progress(bookings, progress_values):
    return sum(1 for booking in bookings if booking.progress in progress_values)


def _format_datetime(value):
    return timezone.localtime(value).strftime("%b %d, %Y").replace(" 0", " ")
