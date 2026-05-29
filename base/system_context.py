from base.models import SystemSettings


DEFAULT_HOME_DESCRIPTION = (
    "Professional construction and maintenance services at your fingertips. "
    "Book online, get detailed quotations, and track your project in real time."
)


def current_system_settings():
    return SystemSettings.objects.order_by("-pk").first()


def home_content():
    settings = current_system_settings()
    tagline = (settings.tagline or "").strip() if settings else ""
    description = (settings.description or "").strip() if settings else ""

    return {
        "tagline": tagline,
        "description": description or DEFAULT_HOME_DESCRIPTION,
        "has_custom_tagline": bool(tagline),
    }


def system_settings_form():
    settings = current_system_settings()

    return {
        "tagline": settings.tagline if settings and settings.tagline else "",
        "description": settings.description if settings and settings.description else "",
        "default_tagline": "Build Better. Maintain Smarter.",
        "default_description": DEFAULT_HOME_DESCRIPTION,
    }
