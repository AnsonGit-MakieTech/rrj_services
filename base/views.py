from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from apis.admin_dashboard import get_admin_booking_detail, get_admin_dashboard_context
from apis.authentications import api_login, api_register, logout_page
from apis.booking_messaging import booking_messages, get_booking_messages
from apis.booking_transactions import (
    decide_booking_quotation,
    submit_booking_payment,
    submit_booking_quotation,
    update_booking_status,
    verify_booking_payment,
)
from apis.manage_booking import create_booking
from apis.manage_service import create_service, delete_service, toggle_service_status, update_service
from apis.my_booking import get_my_booking_context
from base.models import BookingRequest, Service


BOOKINGS = [
    {
        "reference": "BK-MPL5LPV3",
        "service": "Carpentry",
        "status": "Pending Quotation",
        "date": "May 25, 2026",
        "description": "",
        "email": "techmakie@gmail.com",
        "phone": "-",
        "location": "-",
        "sqm": "-",
        "urgency": "High",
        "schedule": "-",
        "attachment_url": "https://images.unsplash.com/photo-1601058268499-e52658b8bb88?auto=format&fit=crop&w=180&q=80",
        "quotation": {
            "materials": "PHP 100",
            "labor": "PHP 400",
            "total": "PHP 500",
            "notes": "Quotation prepared after project assessment.",
        },
    },
    {
        "reference": "BK-MPKPRA6C",
        "service": "Sculpture Maker",
        "status": "Pending Quotation",
        "date": "May 25, 2026",
        "description": "fasdfsdf",
        "email": "techmakie@gmail.com",
        "phone": "09512213004",
        "location": "Manila",
        "sqm": "21",
        "urgency": "Medium",
        "schedule": "-",
        "attachment_url": "",
        "quotation": {
            "materials": "PHP 2,500",
            "labor": "PHP 6,500",
            "total": "PHP 9,000",
            "notes": "Final schedule follows confirmed payment.",
        },
    },
]

# Change this value and refresh a booking detail page to preview a workflow state.
# Available values: pending_quotation, quotation_sent, waiting_for_payment,
# payment_verification, booking_confirmed, scheduled, in_progress, completed,
# cancelled.
SIMULATED_VIEW_BOOKING_STATUS = "payment_verification"

PROGRESS_STEPS = [
    "Pending Quotation",
    "Quotation Sent",
    "Waiting for Payment",
    "Payment Verification",
    "Booking Confirmed",
    "Scheduled",
    "In Progress",
    "Completed",
]

BOOKING_VIEW_STATES = {
    "pending_quotation": {
        "label": "Pending Quotation",
        "variant": "pending",
        "step": 0,
        "show_quotation": False,
        "allow_decision": False,
        "show_payment": False,
    },
    "quotation_sent": {
        "label": "Quotation Sent",
        "variant": "sent",
        "step": 1,
        "show_quotation": True,
        "allow_decision": True,
        "show_payment": False,
    },
    "waiting_for_payment": {
        "label": "Waiting for Payment",
        "variant": "payment",
        "step": 2,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": True,
    },
    "payment_verification": {
        "label": "Payment Verification",
        "variant": "active",
        "step": 3,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": False,
    },
    "booking_confirmed": {
        "label": "Booking Confirmed",
        "variant": "active",
        "step": 4,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": False,
    },
    "scheduled": {
        "label": "Scheduled",
        "variant": "active",
        "step": 5,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": False,
    },
    "in_progress": {
        "label": "In Progress",
        "variant": "active",
        "step": 6,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": False,
    },
    "completed": {
        "label": "Completed",
        "variant": "completed",
        "step": 7,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": False,
    },
    "cancelled": {
        "label": "Cancelled",
        "variant": "cancelled",
        "step": None,
        "show_quotation": True,
        "allow_decision": False,
        "show_payment": False,
    },
}

ADMIN_BOOKING_STATES = {
    "pending_quotation": {
        "label": "Pending Quotation",
        "variant": "pending",
        "status_kind": "pending",
        "step": 0,
        "show_send_quotation": True,
        "show_quotation": False,
        "show_payment_verification": False,
        "show_status_actions": False,
        "status_actions": [],
    },
    "quotation_sent": {
        "label": "Quotation Sent",
        "variant": "sent",
        "status_kind": "pending",
        "step": 1,
        "show_send_quotation": False,
        "show_quotation": True,
        "show_payment_verification": False,
        "show_status_actions": False,
        "status_actions": [],
    },
    "waiting_for_payment": {
        "label": "Waiting for Payment",
        "variant": "payment",
        "status_kind": "payment",
        "step": 2,
        "show_send_quotation": False,
        "show_quotation": True,
        "show_payment_verification": False,
        "show_status_actions": False,
        "status_actions": [],
    },
    "payment_verification": {
        "label": "Payment Verification",
        "variant": "payment",
        "status_kind": "payment",
        "step": 3,
        "show_send_quotation": False,
        "show_quotation": True,
        "show_payment_verification": True,
        "show_status_actions": False,
        "status_actions": [],
    },
    "booking_confirmed": {
        "label": "Booking Confirmed",
        "variant": "active",
        "status_kind": "confirmed",
        "step": 4,
        "show_send_quotation": False,
        "show_quotation": True,
        "show_payment_verification": False,
        "show_status_actions": True,
        "status_actions": [{"label": "Scheduled", "value": "scheduled"}],
    },
    "scheduled": {
        "label": "Scheduled",
        "variant": "active",
        "status_kind": "confirmed",
        "step": 5,
        "show_send_quotation": False,
        "show_quotation": True,
        "show_payment_verification": False,
        "show_status_actions": True,
        "status_actions": [
            {"label": "In Progress", "value": "in_progress"},
            {"label": "Completed", "value": "completed"},
        ],
    },
    "in_progress": {
        "label": "In Progress",
        "variant": "active",
        "status_kind": "confirmed",
        "step": 6,
        "show_send_quotation": False,
        "show_quotation": True,
        "show_payment_verification": False,
        "show_status_actions": True,
        "status_actions": [
            {"label": "Scheduled", "value": "scheduled"},
            {"label": "Completed", "value": "completed"},
        ],
    },
    "completed": {
        "label": "Completed",
        "variant": "completed",
        "status_kind": "completed",
        "step": 7,
        "show_send_quotation": False,
        "show_quotation": True,
        "show_payment_verification": False,
        "show_status_actions": False,
        "status_actions": [],
    },
    "cancelled": {
        "label": "Cancelled",
        "variant": "cancelled",
        "status_kind": "cancelled",
        "step": None,
        "show_send_quotation": False,
        "show_quotation": True,
        "show_payment_verification": False,
        "show_status_actions": False,
        "status_actions": [],
    },
}


def _simulated_state():
    return BOOKING_VIEW_STATES.get(
        SIMULATED_VIEW_BOOKING_STATUS,
        BOOKING_VIEW_STATES["pending_quotation"],
    )


def _admin_state_for_progress(progress):
    return ADMIN_BOOKING_STATES.get(progress, ADMIN_BOOKING_STATES["pending_quotation"])


def _progress_steps(state):
    if state["variant"] == "cancelled":
        return [{"label": "Cancelled", "phase": "cancelled"}]

    steps = []
    for index, label in enumerate(PROGRESS_STEPS):
        if index < state["step"]:
            phase = "complete"
        elif index == state["step"]:
            phase = "current"
        else:
            phase = "upcoming"
        steps.append({"label": label, "phase": phase})
    return steps


def _booking_request_detail(booking):
    attachments = [
        {
            "name": attachment.file.name.rsplit("/", 1)[-1],
            "url": attachment.file.url,
        }
        for attachment in booking.attachments.all()
        if attachment.file
    ]

    return {
        "reference": booking.reference_number,
        "service": booking.service.name,
        "status": booking.get_progress_display(),
        "email": booking.email or "-",
        "phone": booking.contact_number or "-",
        "location": booking.project_location or booking.full_address or "-",
        "sqm": booking.square_meters or "-",
        "urgency": booking.get_urgency_level_display(),
        "schedule": booking.preferred_date or "-",
        "description": booking.problem_description or booking.service_description,
        "attachments": attachments,
        "attachment_url": attachments[0]["url"] if attachments else "",
        "quotation": {
            "materials": f"PHP {booking.material_cost:,.0f}",
            "labor": f"PHP {booking.labor_cost:,.0f}",
            "total": f"PHP {booking.total_cost:,.0f}",
            "notes": booking.transaction_notes or "Quotation details will appear here.",
        },
        "payment": {
            "amount": f"PHP {booking.amount_paid:,.0f}",
            "method": booking.get_payment_method_display(),
            "reference": booking.payment_reference_number or "-",
            "receipt_url": booking.receipt_screenshot.url if booking.receipt_screenshot else "",
        },
    }


def _display_name(request):
    if request.user.is_authenticated:
        return getattr(request.user, "full_name", "") or request.user.get_full_name() or request.user.username
    return "Makie Tech"


def _is_admin(request):
    return request.user.is_authenticated and request.user.is_staff


def _service_queryset(visible_only=True):
    services = Service.objects.filter(is_deleted=False).order_by("name")
    if visible_only:
        services = services.filter(is_active=True)
    return services


def _service_cards(limit=None):
    services = _service_queryset()
    if limit:
        services = services[:limit]

    return [
        {
            "name": service.name,
            "description": service.description,
            "price": service.price_range,
            "image_url": service.display_image_url,
        }
        for service in services
    ]


@login_required
def home(request):
    return render(
        request,
        "base/home.html",
        {
            "active_page": "home",
            "display_name": _display_name(request),
            "is_admin": _is_admin(request),
            "services": _service_cards(limit=8),
        },
    )


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "base/login.html")


def register_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "base/register.html")


@login_required
def admin_dashboard(request):
    if not _is_admin(request):
        raise Http404("Admin dashboard not available")

    dashboard_context = get_admin_dashboard_context()
    dashboard_context.update(
        {
            "active_page": "admin",
            "display_name": _display_name(request),
            "is_admin": True,
        }
    )
    return render(
        request,
        "base/admin.html",
        dashboard_context,
    )


@login_required
def admin_view_booking(request, reference):
    if not _is_admin(request):
        raise Http404("Admin booking not available")

    booking_request = (
        BookingRequest.objects.filter(reference_number=reference)
        .select_related("owner", "service")
        .first()
    )
    if booking_request is None:
        raise Http404("Booking not found")

    booking = get_admin_booking_detail(reference)
    if booking is None:
        raise Http404("Booking not found")

    state = _admin_state_for_progress(booking["progress_key"])
    booking["status"] = state["label"]

    return render(
        request,
        "base/admin_view_booking.html",
        {
            "active_page": "admin",
            "display_name": _display_name(request),
            "is_admin": True,
            "booking": booking,
            "state": state,
            "progress_steps": _progress_steps(state),
            "chat_messages": get_booking_messages(booking_request, request.user),
            "messages_endpoint": reverse("booking_messages", args=[reference]),
            "quotation_submit_endpoint": reverse("submit_booking_quotation", args=[reference]),
            "payment_verify_endpoint": reverse("verify_booking_payment", args=[reference]),
            "status_update_endpoint": reverse("update_booking_status", args=[reference]),
        },
    )


@login_required
def service_settings(request):
    if not _is_admin(request):
        raise Http404("Service settings not available")

    return render(
        request,
        "base/settings.html",
        {
            "active_page": "settings",
            "display_name": _display_name(request),
            "is_admin": True,
            "admin_services": _service_queryset(visible_only=False),
            "service_status_choices": Service._meta.get_field("status").choices,
        },
    )


@login_required
def services(request):
    return render(
        request,
        "base/services.html",
        {
            "active_page": "services",
            "display_name": _display_name(request),
            "is_admin": _is_admin(request),
            "services": _service_cards(),
        },
    )


@login_required
def my_bookings(request):
    booking_context = get_my_booking_context(request.user)
    booking_context.update(
        {
            "active_page": "bookings",
            "display_name": _display_name(request),
            "is_admin": _is_admin(request),
        }
    )

    return render(
        request,
        "base/my_bookings.html",
        booking_context,
    )


@login_required
def add_booking(request):
    selected_service = request.GET.get("service", "")
    services = _service_queryset()
    selected_service_obj = next((service for service in services if service.name == selected_service), None)
    if selected_service_obj is None:
        selected_service = ""

    return render(
        request,
        "base/add_booking.html",
        {
            "active_page": "",
            "display_name": _display_name(request),
            "is_admin": _is_admin(request),
            "services": services,
            "selected_service": selected_service,
            "selected_service_id": selected_service_obj.id if selected_service_obj else "",
            "selected_service_label": selected_service_obj.name if selected_service_obj else "",
            "user_email": request.user.email or "",
            "user_contact_number": getattr(request.user, "contact_number", "") or "",
            "user_full_address": getattr(request.user, "full_address", "") or "",
        },
    )


@login_required
def view_booking(request, reference):
    booking_request = (
        BookingRequest.objects.filter(owner=request.user, reference_number=reference)
        .select_related("service")
        .prefetch_related("attachments")
        .first()
    )
    if booking_request:
        state = BOOKING_VIEW_STATES.get(booking_request.progress, BOOKING_VIEW_STATES["pending_quotation"])
        booking = _booking_request_detail(booking_request)
        return render(
            request,
            "base/view_booking.html",
            {
                "active_page": "bookings",
                "display_name": _display_name(request),
                "is_admin": _is_admin(request),
                "booking": booking,
                "state": state,
                "progress_steps": _progress_steps(state),
                "chat_messages": get_booking_messages(booking_request, request.user),
                "messages_endpoint": reverse("booking_messages", args=[reference]),
                "quotation_decision_endpoint": reverse("decide_booking_quotation", args=[reference]),
                "payment_submit_endpoint": reverse("submit_booking_payment", args=[reference]),
            },
        )

    booking = next((booking.copy() for booking in BOOKINGS if booking["reference"] == reference), None)
    if booking is None:
        raise Http404("Booking not found")

    state = _simulated_state()
    booking["status"] = state["label"]

    return render(
        request,
        "base/view_booking.html",
        {
            "active_page": "bookings",
            "display_name": _display_name(request),
            "is_admin": _is_admin(request),
            "booking": booking,
            "state": state,
            "progress_steps": _progress_steps(state),
            "chat_messages": [],
            "messages_endpoint": reverse("booking_messages", args=[reference]),
            "quotation_decision_endpoint": reverse("decide_booking_quotation", args=[reference]),
            "payment_submit_endpoint": reverse("submit_booking_payment", args=[reference]),
        },
    )
