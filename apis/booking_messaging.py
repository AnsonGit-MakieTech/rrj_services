from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from base.models import BookingRequest, ChatMessage


@login_required
@require_http_methods(["GET", "POST"])
def booking_messages(request, reference):
    booking = _get_accessible_booking(request.user, reference)
    if booking is None:
        raise Http404("Booking not found")

    if request.method == "GET":
        return JsonResponse(
            {
                "success": True,
                "messages": get_booking_messages(booking, request.user),
            }
        )

    message = (request.POST.get("message") or "").strip()
    if not message:
        return JsonResponse(
            {"success": False, "message": "Message cannot be empty."},
            status=400,
        )

    chat_message = ChatMessage.objects.create(
        booking_request=booking,
        message=message,
        sender=request.user,
        receiver=_message_receiver(booking, request.user),
    )

    return JsonResponse(
        {
            "success": True,
            "message": _message_payload(chat_message, request.user),
        },
        status=201,
    )


def get_booking_messages(booking, current_user):
    return [
        _message_payload(message, current_user)
        for message in booking.chat_messages.select_related("sender", "receiver").order_by("created_at", "id")
    ]


def _get_accessible_booking(user, reference):
    queryset = BookingRequest.objects.select_related("owner", "service")
    if user.is_staff:
        return queryset.filter(reference_number=reference).first()
    return queryset.filter(reference_number=reference, owner=user).first()


def _message_receiver(booking, sender):
    if sender.is_staff:
        return booking.owner if booking.owner_id != sender.id else None

    User = get_user_model()
    return User.objects.filter(is_staff=True, is_active=True).exclude(id=sender.id).order_by("id").first()


def _message_payload(message, current_user):
    created_at = timezone.localtime(message.created_at)
    is_admin_sender = message.sender.is_staff
    return {
        "id": message.id,
        "message": message.message or "",
        "sender_label": "RRJ Admin" if is_admin_sender else _user_label(message.sender),
        "sender_role": "admin" if is_admin_sender else "customer",
        "is_own": message.sender_id == current_user.id,
        "created_at": created_at.strftime("%b %d, %Y %I:%M %p").replace(" 0", " "),
        "created_at_iso": created_at.isoformat(),
    }


def _user_label(user):
    return getattr(user, "full_name", "") or user.get_full_name() or user.username
