from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST

from base.models import BookingRequest, ChatMessage


MAX_RECEIPT_SIZE = 10 * 1024 * 1024
ALLOWED_RECEIPT_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
STATUS_TRANSITIONS = {
    "booking_confirmed": {"scheduled"},
    "scheduled": {"in_progress", "completed"},
    "in_progress": {"scheduled", "completed"},
}
STATUS_UPDATE_MESSAGES = {
    "scheduled": "Booking scheduled. RRJ Admin updated the project status to Scheduled.",
    "in_progress": "Work is now in progress. RRJ Admin updated the project status to In Progress.",
    "completed": "Project marked as completed. RRJ Admin updated the booking status to Completed.",
}


@login_required
@require_POST
def submit_booking_quotation(request, reference):
    if not request.user.is_staff:
        raise Http404("Quotation submission not available")

    material_cost, material_error = _parse_money(request, "materials_cost", "Materials cost")
    labor_cost, labor_error = _parse_money(request, "labor_cost", "Labor cost")
    total_cost, total_error = _parse_money(request, "total_amount", "Total amount", required=True)
    error = material_error or labor_error or total_error
    if error:
        return JsonResponse({"success": False, "message": error}, status=400)

    if total_cost <= 0:
        return JsonResponse(
            {"success": False, "message": "Total amount must be greater than zero."},
            status=400,
        )

    notes = (request.POST.get("notes") or "").strip()

    with transaction.atomic():
        booking = (
            BookingRequest.objects.select_for_update()
            .select_related("owner", "service")
            .filter(reference_number=reference)
            .first()
        )
        if booking is None:
            raise Http404("Booking not found")
        if booking.progress != "pending_quotation":
            return JsonResponse(
                {"success": False, "message": "Quotation can only be sent while the request is pending quotation."},
                status=400,
            )

        booking.material_cost = float(material_cost)
        booking.labor_cost = float(labor_cost)
        booking.total_cost = float(total_cost)
        booking.transaction_notes = notes
        booking.progress = "quotation_sent"
        booking.save(
            update_fields=[
                "material_cost",
                "labor_cost",
                "total_cost",
                "transaction_notes",
                "progress",
                "updated_at",
            ]
        )
        ChatMessage.objects.create(
            booking_request=booking,
            sender=request.user,
            receiver=booking.owner,
            message=_quotation_sent_message(booking),
        )

    return JsonResponse(
        {
            "success": True,
            "message": "Quotation sent to customer.",
            "status": "Quotation Sent",
            "redirect_url": reverse("admin_view_booking", args=[reference]),
        }
    )


@login_required
@require_POST
def decide_booking_quotation(request, reference):
    decision = (request.POST.get("decision") or "").strip().lower()
    if decision not in {"accept", "reject"}:
        return JsonResponse({"success": False, "message": "Please accept or reject the quotation."}, status=400)

    with transaction.atomic():
        booking = (
            BookingRequest.objects.select_for_update()
            .select_related("owner", "service")
            .filter(reference_number=reference, owner=request.user)
            .first()
        )
        if booking is None:
            raise Http404("Booking not found")
        if booking.progress != "quotation_sent":
            return JsonResponse(
                {"success": False, "message": "This quotation is no longer waiting for your decision."},
                status=400,
            )

        if decision == "accept":
            booking.progress = "waiting_for_payment"
            message = "Quotation accepted. Waiting for payment proof."
            status = "Waiting for Payment"
        else:
            booking.progress = "pending_quotation"
            message = "Quotation rejected. Please review and send an updated quotation."
            status = "Pending Quotation"

        booking.save(update_fields=["progress", "updated_at"])
        ChatMessage.objects.create(
            booking_request=booking,
            sender=request.user,
            receiver=_first_admin_user(request.user),
            message=message,
        )

    return JsonResponse(
        {
            "success": True,
            "message": message,
            "status": status,
            "redirect_url": reverse("view_booking", args=[reference]),
        }
    )


@login_required
@require_POST
def submit_booking_payment(request, reference):
    amount_paid, amount_error = _parse_money(request, "amount_paid", "Amount paid", required=True)
    if amount_error:
        return JsonResponse({"success": False, "message": amount_error}, status=400)
    if amount_paid <= 0:
        return JsonResponse(
            {"success": False, "message": "Amount paid must be greater than zero."},
            status=400,
        )

    payment_method = (request.POST.get("payment_method") or "").strip()
    valid_payment_methods = {value for value, _ in BookingRequest._meta.get_field("payment_method").choices}
    if payment_method not in valid_payment_methods:
        return JsonResponse({"success": False, "message": "Please select a valid payment method."}, status=400)

    receipt = request.FILES.get("receipt")
    receipt_error = _validate_receipt(receipt)
    if receipt_error:
        return JsonResponse({"success": False, "message": receipt_error}, status=400)

    payment_reference = (request.POST.get("payment_reference_number") or "").strip()

    with transaction.atomic():
        booking = (
            BookingRequest.objects.select_for_update()
            .select_related("owner", "service")
            .filter(reference_number=reference, owner=request.user)
            .first()
        )
        if booking is None:
            raise Http404("Booking not found")
        if booking.progress != "waiting_for_payment":
            return JsonResponse(
                {"success": False, "message": "Payment proof can only be submitted while waiting for payment."},
                status=400,
            )

        booking.amount_paid = float(amount_paid)
        booking.payment_method = payment_method
        booking.payment_reference_number = payment_reference
        booking.receipt_screenshot = receipt
        booking.approved_payment = False
        booking.progress = "payment_verification"
        booking.save(
            update_fields=[
                "amount_paid",
                "payment_method",
                "payment_reference_number",
                "receipt_screenshot",
                "approved_payment",
                "progress",
                "updated_at",
            ]
        )
        ChatMessage.objects.create(
            booking_request=booking,
            sender=request.user,
            receiver=_first_admin_user(request.user),
            message=f"Payment proof submitted. Amount paid: {_format_money(booking.amount_paid)}.",
        )

    return JsonResponse(
        {
            "success": True,
            "message": "Payment proof submitted for admin verification.",
            "status": "Payment Verification",
            "redirect_url": reverse("view_booking", args=[reference]),
        }
    )


@login_required
@require_POST
def verify_booking_payment(request, reference):
    if not request.user.is_staff:
        raise Http404("Payment verification not available")

    decision = (request.POST.get("decision") or "").strip().lower()
    if decision not in {"approve", "reject"}:
        return JsonResponse({"success": False, "message": "Please approve or reject the payment."}, status=400)

    with transaction.atomic():
        booking = (
            BookingRequest.objects.select_for_update()
            .select_related("owner", "service")
            .filter(reference_number=reference)
            .first()
        )
        if booking is None:
            raise Http404("Booking not found")
        if booking.progress != "payment_verification":
            return JsonResponse(
                {"success": False, "message": "This booking is not waiting for payment verification."},
                status=400,
            )

        if decision == "approve":
            booking.approved_payment = True
            booking.progress = "booking_confirmed"
            message = "Payment approved. Booking confirmed."
            status = "Booking Confirmed"
        else:
            booking.approved_payment = False
            booking.progress = "waiting_for_payment"
            message = "Payment proof rejected. Please upload a new receipt for verification."
            status = "Waiting for Payment"

        booking.save(update_fields=["approved_payment", "progress", "updated_at"])
        ChatMessage.objects.create(
            booking_request=booking,
            sender=request.user,
            receiver=booking.owner,
            message=message,
        )

    return JsonResponse(
        {
            "success": True,
            "message": message,
            "status": status,
            "redirect_url": reverse("admin_view_booking", args=[reference]),
        }
    )


@login_required
@require_POST
def update_booking_status(request, reference):
    if not request.user.is_staff:
        raise Http404("Booking status update not available")

    target_progress = (request.POST.get("progress") or "").strip()
    progress_labels = dict(BookingRequest._meta.get_field("progress").choices)
    if target_progress not in progress_labels:
        return JsonResponse({"success": False, "message": "Please select a valid booking status."}, status=400)

    with transaction.atomic():
        booking = (
            BookingRequest.objects.select_for_update()
            .select_related("owner", "service")
            .filter(reference_number=reference)
            .first()
        )
        if booking is None:
            raise Http404("Booking not found")

        allowed_targets = STATUS_TRANSITIONS.get(booking.progress, set())
        if target_progress not in allowed_targets:
            return JsonResponse(
                {"success": False, "message": "That status update is not allowed for the current booking state."},
                status=400,
            )

        booking.progress = target_progress
        booking.save(update_fields=["progress", "updated_at"])
        message = STATUS_UPDATE_MESSAGES.get(
            target_progress,
            f"Booking status updated to {progress_labels[target_progress]}.",
        )
        ChatMessage.objects.create(
            booking_request=booking,
            sender=request.user,
            receiver=booking.owner,
            message=message,
        )

    return JsonResponse(
        {
            "success": True,
            "message": message,
            "status": progress_labels[target_progress],
            "redirect_url": reverse("admin_view_booking", args=[reference]),
        }
    )


def _parse_money(request, field_name, label, required=False):
    raw_value = (request.POST.get(field_name) or "").strip().replace(",", "")
    if not raw_value:
        if required:
            return None, f"{label} is required."
        return Decimal("0"), None

    try:
        value = Decimal(raw_value)
    except (InvalidOperation, ValueError):
        return None, f"{label} must be a valid amount."

    if value < 0:
        return None, f"{label} cannot be negative."

    return value, None


def _validate_receipt(receipt):
    if receipt is None:
        return "Receipt screenshot is required."

    extension = Path(receipt.name).suffix.lower()
    if extension not in ALLOWED_RECEIPT_EXTENSIONS:
        return "Only JPG, PNG, and WEBP receipts are accepted."
    if receipt.size > MAX_RECEIPT_SIZE:
        return "Receipt must be 10MB or smaller."
    if receipt.content_type and not receipt.content_type.startswith("image/"):
        return "Only image receipt files are accepted."

    return ""


def _quotation_sent_message(booking):
    total = _format_money(booking.total_cost)
    message = f"Quotation sent for {booking.service.name}. Total: {total}."
    if booking.transaction_notes:
        message = f"{message} Notes: {booking.transaction_notes}"
    return message


def _format_money(value):
    return f"PHP {float(value or 0):,.0f}"


def _first_admin_user(sender):
    User = get_user_model()
    return User.objects.filter(is_staff=True, is_active=True).exclude(id=sender.id).order_by("id").first()
