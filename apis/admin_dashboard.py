from collections import OrderedDict

from django.db.models import Sum
from django.utils import timezone

from base.models import BookingRequest


ACTIVE_PROGRESS = {"booking_confirmed", "scheduled", "in_progress"}
STATUS_KIND_BY_PROGRESS = {
    "pending_quotation": "pending",
    "quotation_sent": "pending",
    "waiting_for_payment": "payment",
    "payment_verification": "payment",
    "booking_confirmed": "confirmed",
    "scheduled": "confirmed",
    "in_progress": "confirmed",
    "completed": "completed",
    "cancelled": "cancelled",
}


def get_admin_dashboard_context():
    bookings = list(
        BookingRequest.objects.select_related("owner", "service")
        .prefetch_related("attachments")
        .order_by("-created_at")
    )
    revenue = BookingRequest.objects.aggregate(total=Sum("amount_paid"))["total"] or 0

    return {
        "admin_stats": [
            {"label": "Total Bookings", "value": str(len(bookings)), "kind": "bookings"},
            {
                "label": "Pending Quotations",
                "value": str(_count_progress(bookings, {"pending_quotation"})),
                "kind": "pending",
            },
            {
                "label": "Active Jobs",
                "value": str(_count_progress(bookings, ACTIVE_PROGRESS)),
                "kind": "active",
            },
            {"label": "Revenue", "value": _format_money(revenue), "kind": "revenue"},
        ],
        "admin_bookings": [_booking_row(booking) for booking in bookings],
        "admin_monthly_chart": _monthly_chart(bookings),
        "admin_service_chart": _service_chart(bookings),
        "admin_status_options": _status_options(),
    }


def get_admin_booking_detail(reference):
    booking = (
        BookingRequest.objects.filter(reference_number=reference)
        .select_related("owner", "service")
        .prefetch_related("attachments")
        .first()
    )
    if booking is None:
        return None

    return {
        "reference": booking.reference_number,
        "progress_key": booking.progress,
        "customer": _customer_name(booking),
        "service": booking.service.name,
        "status": booking.get_progress_display(),
        "email": booking.email or "-",
        "phone": booking.contact_number or "-",
        "location": booking.project_location or booking.full_address or "-",
        "sqm": booking.square_meters or "-",
        "urgency": booking.get_urgency_level_display(),
        "schedule": _format_date(booking.preferred_date),
        "description": booking.problem_description or booking.service_description,
        "attachments": _attachments(booking),
        "quotation": {
            "materials": _format_money(booking.material_cost),
            "labor": _format_money(booking.labor_cost),
            "total": _format_money(booking.total_cost),
            "materials_value": _format_input_money(booking.material_cost),
            "labor_value": _format_input_money(booking.labor_cost),
            "total_value": _format_input_money(booking.total_cost),
            "notes": booking.transaction_notes or "Quotation details will appear here.",
            "notes_value": booking.transaction_notes or "",
        },
        "payment": {
            "amount": _format_money(booking.amount_paid),
            "method": booking.get_payment_method_display(),
            "reference": booking.payment_reference_number or "-",
            "receipt_url": booking.receipt_screenshot.url if booking.receipt_screenshot else "",
        },
    }


def _booking_row(booking):
    return {
        "reference": booking.reference_number,
        "customer": _customer_name(booking),
        "service": booking.service.name,
        "status": booking.get_progress_display(),
        "status_kind": STATUS_KIND_BY_PROGRESS.get(booking.progress, "pending"),
        "date": _format_datetime(booking.created_at),
    }


def _monthly_chart(bookings):
    counts = OrderedDict()
    for booking in sorted(bookings, key=lambda item: item.created_at):
        label = timezone.localtime(booking.created_at).strftime("%b")
        counts[label] = counts.get(label, 0) + 1

    items = [{"label": label, "value": value} for label, value in counts.items()]
    if not items:
        items = [{"label": "No data", "value": 0}]

    return {
        "labels": [item["label"] for item in items],
        "values": [item["value"] for item in items],
        "items": items,
    }


def _service_chart(bookings):
    counts = {}
    for booking in bookings:
        service_name = booking.service.name
        counts[service_name] = counts.get(service_name, 0) + 1

    items = [
        {"label": label, "value": value}
        for label, value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    if not items:
        items = [{"label": "No data", "value": 0}]

    return {
        "labels": [item["label"] for item in items],
        "values": [item["value"] for item in items],
        "items": items,
    }


def _status_options():
    return [
        {"label": "All Statuses", "value": ""},
        *[
            {"label": label, "value": label}
            for _, label in BookingRequest._meta.get_field("progress").choices
        ],
    ]


def _attachments(booking):
    return [
        {
            "name": attachment.file.name.rsplit("/", 1)[-1],
            "url": attachment.file.url,
        }
        for attachment in booking.attachments.all()
        if attachment.file
    ]


def _customer_name(booking):
    owner_name = getattr(booking.owner, "full_name", "") or booking.owner.get_full_name() or booking.owner.username
    return booking.full_name or owner_name


def _count_progress(bookings, progress_values):
    return sum(1 for booking in bookings if booking.progress in progress_values)


def _format_money(value):
    return f"PHP {float(value or 0):,.0f}"


def _format_input_money(value):
    amount = float(value or 0)
    if amount == 0:
        return ""
    return f"{amount:.2f}".rstrip("0").rstrip(".")


def _format_datetime(value):
    return timezone.localtime(value).strftime("%b %d, %Y").replace(" 0", " ")


def _format_date(value):
    if not value:
        return "-"
    return value.strftime("%b %d, %Y").replace(" 0", " ")
