from base.models import Service


def service_queryset(visible_only=True):
    services = Service.objects.filter(is_deleted=False).order_by("name")
    if visible_only:
        services = services.filter(is_active=True)
    return services


def service_cards(limit=None):
    services = service_queryset()
    if limit:
        services = services[:limit]

    return [
        {
            "name": service.name,
            "description": service.description,
            "price": service.price_range,
            "image_url": service.display_image_url,
        }
        for service in services
    ]


def service_status_choices():
    return Service._meta.get_field("status").choices
