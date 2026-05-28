from django.contrib import admin
from base.models import *
# Register your models here.


class AuthenticatedUserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "contact_number")
    search_fields = ("full_name", "contact_number")
    ordering = ("full_name",)


class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ("tagline", "description")
    search_fields = ("tagline", "description")
    ordering = ("tagline",)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "min_price", "max_price", "is_active", "image")
    search_fields = ("name", "description", "min_price", "max_price", "image")
    ordering = ("name",)


class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ("owner", "progress", "created_at", "updated_at")
    search_fields = ("owner__full_name", "owner__contact_number", "service__name", "reference_number")
    ordering = ("-created_at",)


class BookingAttachmentAdmin(admin.ModelAdmin):
    list_display = ("booking_request", "created_at", "updated_at")
    search_fields = ("booking_request__owner__full_name", "booking_request__owner__contact_number", "file")
    ordering = ("-created_at",)


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("booking_request", "created_at", "updated_at")
    search_fields = ("booking_request__owner__full_name", "booking_request__owner__contact_number", "message")
    ordering = ("-created_at",)


admin.site.register(AuthenticatedUser, AuthenticatedUserAdmin)
admin.site.register(SystemSettings, SystemSettingsAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(BookingRequest, BookingRequestAdmin)
admin.site.register(BookingAttachment, BookingAttachmentAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)

 