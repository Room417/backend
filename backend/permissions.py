from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


class StaffUserPermission(IsAuthenticated):
    def has_permission(self, request, view):
        """ Авторизован ли пользователь, как staff """
        if not super().has_permission(request, view):
            return False

        try:
            request.user.staff
            return True
        except User.staff.RelatedObjectDoesNotExist:
            return False
