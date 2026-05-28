from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from base.models import Service


@require_POST
def create_service(request):
    _require_staff(request)

    name = request.POST.get("name", "").strip()
    if not name:
        messages.error(request, "Service name is required.")
        return redirect("service_settings")

    service = Service(
        name=name,
        description=request.POST.get("description", "").strip(),
        min_price=_clean_price(request.POST.get("min_price")),
        max_price=_clean_price(request.POST.get("max_price")),
        status=_clean_status(request.POST.get("status")),
        is_active=_is_checked(request, "is_active"),
    )

    if request.FILES.get("image"):
        service.image = request.FILES["image"]

    service.save()
    messages.success(request, "Service created.")
    return redirect("service_settings")


@require_POST
def update_service(request):
    _require_staff(request)

    service = get_object_or_404(
        Service,
        pk=request.POST.get("service_id"),
        is_deleted=False,
    )

    name = request.POST.get("name", "").strip()
    if not name:
        messages.error(request, "Service name is required.")
        return redirect("service_settings")

    service.name = name
    service.description = request.POST.get("description", "").strip()
    service.min_price = _clean_price(request.POST.get("min_price"))
    service.max_price = _clean_price(request.POST.get("max_price"))
    service.status = _clean_status(request.POST.get("status"))
    service.is_active = _is_checked(request, "is_active")

    if request.FILES.get("image"):
        service.image = request.FILES["image"]

    service.save()
    messages.success(request, "Service updated.")
    return redirect("service_settings")


@require_POST
def toggle_service_status(request, service_id):
    _require_staff(request)

    service = get_object_or_404(Service, pk=service_id, is_deleted=False)
    service.is_active = _is_checked(request, "is_active")
    service.save(update_fields=["is_active"])
    messages.success(request, "Service visibility updated.")
    return redirect("service_settings")


@require_POST
def delete_service(request, service_id):
    _require_staff(request)

    service = get_object_or_404(Service, pk=service_id, is_deleted=False)
    service.is_deleted = True
    service.is_active = False
    service.save(update_fields=["is_deleted", "is_active"])
    messages.success(request, "Service deleted.")
    return redirect("service_settings")


def _require_staff(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        raise Http404("Service management not available")


def _clean_price(value):
    try:
        return max(int(value or 0), 0)
    except (TypeError, ValueError):
        return 0


def _clean_status(value):
    valid_statuses = {choice[0] for choice in Service._meta.get_field("status").choices}
    if value in valid_statuses:
        return value
    return "available"


def _is_checked(request, field_name):
    return request.POST.get(field_name) == "1"
