def display_name(request):
    if request.user.is_authenticated:
        return getattr(request.user, "full_name", "") or request.user.get_full_name() or request.user.username
    return "Makie Tech"


def is_admin(request):
    return request.user.is_authenticated and request.user.is_staff
