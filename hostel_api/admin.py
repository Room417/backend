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
    pass


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass
