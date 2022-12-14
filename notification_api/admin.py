from django.contrib import admin

from .models import (
    Notification,
    Request
)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    """ Админ панель для объектов модели заявок """
    pass


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """ Админ панель для объектов модели уведомлений """
    pass
