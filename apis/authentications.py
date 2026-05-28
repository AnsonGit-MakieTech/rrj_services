import re

from django.contrib.auth import get_user_model, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

def api_login(request):
    full_name = request.POST.get("full_name", "").strip()
    contact_number = _normalize_contact_number(request.POST.get("contact_number", ""))

    if not full_name or not contact_number:
        return JsonResponse(
            {"success": False, "message": "Full name and contact number are required."},
            status=400,
        )

    user = _find_user(full_name, contact_number)
    if user is None:
        return JsonResponse(
            {"success": False, "message": "No account matches those login details."},
            status=401,
        )

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return JsonResponse({"success": True, "redirect_url": _redirect_url(request)})

def api_register(request):
    full_name = request.POST.get("full_name", "").strip()
    contact_number = _normalize_contact_number(request.POST.get("contact_number", ""))

    if not full_name or not contact_number:
        return JsonResponse(
            {"success": False, "message": "Full name and contact number are required."},
            status=400,
        )

    User = get_user_model()
    if User.objects.filter(contact_number=contact_number).exists():
        return JsonResponse(
            {"success": False, "message": "That contact number is already registered. Please login instead."},
            status=409,
        )

    first_name, last_name = _split_name(full_name)
    user = User.objects.create_user(
        username=contact_number,
        password=None,
        first_name=first_name,
        last_name=last_name,
        full_name=full_name,
        contact_number=contact_number,
    )

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return JsonResponse({"success": True, "redirect_url": reverse("home")}, status=201)


def logout_page(request):
    logout(request)
    return redirect("login")


api_login = require_POST(api_login)
api_register = require_POST(api_register)


def _find_user(full_name, contact_number):
    User = get_user_model()
    for user in User.objects.filter(contact_number=contact_number):
        stored_name = (getattr(user, "full_name", "") or user.get_full_name()).strip()
        if stored_name.casefold() == full_name.casefold():
            return user
    return None


def _normalize_contact_number(value):
    digits = re.sub(r"\D", "", value or "")
    if digits.startswith("0") and len(digits) >= 10:
        return "63" + digits[1:]
    if digits.startswith("9") and len(digits) == 10:
        return "63" + digits
    return digits


def _split_name(full_name):
    parts = full_name.split(maxsplit=1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""
    return first_name, last_name


def _redirect_url(request):
    next_url = request.POST.get("next", "")
    if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
        return next_url
    return reverse("home")
