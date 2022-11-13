from django.contrib import admin

from .models import (
    Notification,
    Request
)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass
