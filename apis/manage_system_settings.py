from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from base.models import SystemSettings
from base.system_context import current_system_settings


@require_POST
def update_system_settings(request):
    _require_staff(request)

    settings = current_system_settings() or SystemSettings()
    settings.tagline = request.POST.get("tagline", "").strip()
    settings.description = request.POST.get("description", "").strip()
    settings.save()

    if settings.tagline or settings.description:
        messages.success(request, "Homepage content updated.")
    else:
        messages.success(request, "Homepage content reset to defaults.")

    return redirect("service_settings")


def _require_staff(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        raise Http404("System settings are not available")
