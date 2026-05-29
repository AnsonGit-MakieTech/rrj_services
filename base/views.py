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
from base.booking_context import (
    BOOKING_VIEW_STATES,
    admin_booking_request,
    admin_state_for_progress,
    booking_request_detail,
    customer_booking_request,
    progress_steps,
)
from base.service_context import service_cards, service_queryset, service_status_choices
from base.user_context import display_name, is_admin


@login_required
def home(request):
    return render(
        request,
        "base/home.html",
        {
            "active_page": "home",
            "display_name": display_name(request),
            "is_admin": is_admin(request),
            "services": service_cards(limit=8),
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
    if not is_admin(request):
        raise Http404("Admin dashboard not available")

    dashboard_context = get_admin_dashboard_context()
    dashboard_context.update(
        {
            "active_page": "admin",
            "display_name": display_name(request),
            "is_admin": True,
        }
    )
    return render(request, "base/admin.html", dashboard_context)


@login_required
def admin_view_booking(request, reference):
    if not is_admin(request):
        raise Http404("Admin booking not available")

    booking_request = admin_booking_request(reference)
    if booking_request is None:
        raise Http404("Booking not found")

    booking = get_admin_booking_detail(reference)
    if booking is None:
        raise Http404("Booking not found")

    state = admin_state_for_progress(booking["progress_key"])
    booking["status"] = state["label"]

    return render(
        request,
        "base/admin_view_booking.html",
        {
            "active_page": "admin",
            "display_name": display_name(request),
            "is_admin": True,
            "booking": booking,
            "state": state,
            "progress_steps": progress_steps(state),
            "chat_messages": get_booking_messages(booking_request, request.user),
            "messages_endpoint": reverse("booking_messages", args=[reference]),
            "quotation_submit_endpoint": reverse("submit_booking_quotation", args=[reference]),
            "payment_verify_endpoint": reverse("verify_booking_payment", args=[reference]),
            "status_update_endpoint": reverse("update_booking_status", args=[reference]),
        },
    )


@login_required
def service_settings(request):
    if not is_admin(request):
        raise Http404("Service settings not available")

    return render(
        request,
        "base/settings.html",
        {
            "active_page": "settings",
            "display_name": display_name(request),
            "is_admin": True,
            "admin_services": service_queryset(visible_only=False),
            "service_status_choices": service_status_choices(),
        },
    )


@login_required
def services(request):
    return render(
        request,
        "base/services.html",
        {
            "active_page": "services",
            "display_name": display_name(request),
            "is_admin": is_admin(request),
            "services": service_cards(),
        },
    )


@login_required
def my_bookings(request):
    booking_context = get_my_booking_context(request.user)
    booking_context.update(
        {
            "active_page": "bookings",
            "display_name": display_name(request),
            "is_admin": is_admin(request),
        }
    )

    return render(request, "base/my_bookings.html", booking_context)


@login_required
def add_booking(request):
    selected_service = request.GET.get("service", "")
    services = service_queryset()
    selected_service_obj = services.filter(name=selected_service).first() if selected_service else None
    if selected_service_obj is None:
        selected_service = ""

    return render(
        request,
        "base/add_booking.html",
        {
            "active_page": "",
            "display_name": display_name(request),
            "is_admin": is_admin(request),
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
    booking_request = customer_booking_request(request.user, reference)
    if booking_request:
        state = BOOKING_VIEW_STATES.get(booking_request.progress, BOOKING_VIEW_STATES["pending_quotation"])
        booking = booking_request_detail(booking_request)
        return render(
            request,
            "base/view_booking.html",
            {
                "active_page": "bookings",
                "display_name": display_name(request),
                "is_admin": is_admin(request),
                "booking": booking,
                "state": state,
                "progress_steps": progress_steps(state),
                "chat_messages": get_booking_messages(booking_request, request.user),
                "messages_endpoint": reverse("booking_messages", args=[reference]),
                "quotation_decision_endpoint": reverse("decide_booking_quotation", args=[reference]),
                "payment_submit_endpoint": reverse("submit_booking_payment", args=[reference]),
            },
        )

    raise Http404("Booking not found")
