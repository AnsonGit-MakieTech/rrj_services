import secrets
import string
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST

from base.models import BookingAttachment, BookingRequest, Service


MAX_ATTACHMENTS = 10
MAX_ATTACHMENT_SIZE = 10 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


@require_POST
def create_booking(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "message": "Please login before creating a booking."},
            status=401,
        )

    rate_limit_response = _check_booking_rate_limit(request)
    if rate_limit_response:
        return rate_limit_response

    service = Service.objects.filter(
        pk=request.POST.get("service_id"),
        is_active=True,
        is_deleted=False,
    ).first()
    if service is None:
        return JsonResponse(
            {"success": False, "message": "Please select an available service."},
            status=400,
        )
    if service.status != "available":
        return JsonResponse(
            {"success": False, "message": "This service is not accepting bookings right now."},
            status=400,
        )

    full_name = request.POST.get("full_name", "").strip()
    email = request.POST.get("email", "").strip()
    if not full_name or not email:
        return JsonResponse(
            {"success": False, "message": "Full name and email are required."},
            status=400,
        )

    attachments = request.FILES.getlist("attachments")
    validation_error = _validate_attachments(attachments)
    if validation_error:
        return JsonResponse({"success": False, "message": validation_error}, status=400)

    with transaction.atomic():
        booking = BookingRequest.objects.create(
            owner=request.user,
            reference_number=_generate_reference_number(),
            full_name=full_name,
            email=email,
            contact_number=request.POST.get("contact_number", "").strip(),
            full_address=request.POST.get("full_address", "").strip(),
            service=service,
            urgency_level=_clean_urgency(request.POST.get("urgency_level")),
            preferred_date=parse_date(request.POST.get("preferred_date", "")) or None,
            square_meters=_clean_float(request.POST.get("square_meters")),
            project_location=request.POST.get("project_location", "").strip(),
            service_description=request.POST.get("service_description", "").strip(),
            problem_description=request.POST.get("problem_description", "").strip(),
        )

        for attachment in attachments:
            BookingAttachment.objects.create(
                booking_request=booking,
                file=attachment,
            )

    return JsonResponse(
        {
            "success": True,
            "message": "Booking request submitted.",
            "reference_number": booking.reference_number,
            "redirect_url": reverse("view_booking", args=[booking.reference_number]),
        },
        status=201,
    )


def _check_booking_rate_limit(request):
    request_limit = settings.BOOKING_RATE_LIMIT_REQUESTS
    window_seconds = settings.BOOKING_RATE_LIMIT_WINDOW_SECONDS
    cache_key = f"booking-create-rate-limit:user:{request.user.pk}"

    if cache.add(cache_key, 1, timeout=window_seconds):
        request_count = 1
    else:
        try:
            request_count = cache.incr(cache_key)
        except ValueError:
            cache.set(cache_key, 1, timeout=window_seconds)
            request_count = 1

    remaining = max(request_limit - request_count, 0)
    if request_count <= request_limit:
        return None

    response = JsonResponse(
        {
            "success": False,
            "message": "Too many booking requests. Please try again later.",
        },
        status=429,
    )
    response["Retry-After"] = str(window_seconds)
    response["X-RateLimit-Limit"] = str(request_limit)
    response["X-RateLimit-Remaining"] = str(remaining)
    return response


def _generate_reference_number():
    alphabet = string.ascii_uppercase + string.digits
    while True:
        suffix = "".join(secrets.choice(alphabet) for _ in range(8))
        reference_number = f"BK-{suffix}"
        if not BookingRequest.objects.filter(reference_number=reference_number).exists():
            return reference_number


def _validate_attachments(attachments):
    if len(attachments) > MAX_ATTACHMENTS:
        return f"Upload up to {MAX_ATTACHMENTS} images only."

    for attachment in attachments:
        extension = Path(attachment.name).suffix.lower()
        if extension not in ALLOWED_IMAGE_EXTENSIONS:
            return "Only JPG, PNG, and WEBP images are accepted."
        if attachment.size > MAX_ATTACHMENT_SIZE:
            return "Each image must be 10MB or smaller."
        if attachment.content_type and not attachment.content_type.startswith("image/"):
            return "Only image files are accepted."

    return ""


def _clean_urgency(value):
    valid_values = {choice[0] for choice in BookingRequest._meta.get_field("urgency_level").choices}
    if value in valid_values:
        return value
    return "medium"


def _clean_float(value):
    try:
        return max(float(value or 0), 0)
    except (TypeError, ValueError):
        return 0
