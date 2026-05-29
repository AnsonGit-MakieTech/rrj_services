from base.models import BookingRequest


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


def admin_state_for_progress(progress):
    return ADMIN_BOOKING_STATES.get(progress, ADMIN_BOOKING_STATES["pending_quotation"])


def progress_steps(state):
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


def admin_booking_request(reference):
    return (
        BookingRequest.objects.filter(reference_number=reference)
        .select_related("owner", "service")
        .first()
    )


def customer_booking_request(user, reference):
    return (
        BookingRequest.objects.filter(owner=user, reference_number=reference)
        .select_related("service")
        .prefetch_related("attachments")
        .first()
    )


def booking_request_detail(booking):
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
