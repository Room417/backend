from django.contrib import admin

from .models import (
    Staff,
    Student,
    Resident,
    Room,
    Building,
)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    """ Админ панель для объектов модели сотрудника """
    pass


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    """ Админ панель для объектов модели здания """
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """ Админ панель для объектов модели студента """
    pass


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    """ Админ панель для объектов модели проживающего """
    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """ Админ панель для объектов модели комнаты """
    pass
