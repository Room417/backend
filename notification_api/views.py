from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hostel_api.mixins import DefaultViewMixin
from hostel_api.models import Resident, Staff, Student
from .models import Notification, Request
from .serializers import (
    NotificationSerializer,
    RequestSerializer,
    NotificationCreateSerializer,
    RequestCreateSerializer,
)


class NotificationViewSet(DefaultViewMixin):
    """ ViewSet для взаимодействия с данными работников общежития """
    model = Notification
    serializer_class = NotificationSerializer
    list_serializer = NotificationSerializer
    detail_serializer = NotificationSerializer
    create_serializer = NotificationCreateSerializer
    default_sort_fields = ['-start_date']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            return self.model.objects.filter(author_id=self.request.user.staff.id)
        except User.staff.RelatedObjectDoesNotExist:
            return self.model.objects.filter(recipients__in=[self.request.user.student.resident])

    def create(self, request, *args, **kwargs):
        try:
            staff = self.request.user.staff
            recipients = [
                resident.id for resident in
                Resident.objects.select_related('room').filter(room__building_id__in=staff.buildings.all())
            ]
            data = request.data.copy()
            data['recipients'] = recipients
            data['author'] = staff.id
            serializer = self.create_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except User.staff.RelatedObjectDoesNotExist:
            return Response(data={
                'error': 'У Вас нет доступа к созданию уведомлений',
                'msg': 'Вы не являетесь работником общежития'
            }, status=status.HTTP_403_FORBIDDEN)


class RequestsViewSet(DefaultViewMixin):
    """ ViewSet для взаимодействия с данными работников общежития """
    model = Request
    create_serializer = RequestCreateSerializer
    serializer_class = RequestSerializer
    list_serializer = RequestSerializer
    detail_serializer = RequestSerializer
    default_sort_fields = ['-start_date']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            return self.model.objects.filter(recipients__in=[self.request.user.staff.id])
        except User.staff.RelatedObjectDoesNotExist:
            return self.model.objects.filter(author__in=[self.request.user.student.resident])

    def create(self, request, *args, **kwargs):
        try:
            resident = self.request.user.student.resident
            recipients = [
                resident.id for resident in
                Staff.objects.prefetch_related('buildings').filter(buildings__in=[resident.room.building])
            ]
            data = request.data.copy()
            data['recipients'] = recipients
            data['author'] = resident.id
            serializer = self.create_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except (User.student.RelatedObjectDoesNotExist, Student.resident.RelatedObjectDoesNotExist):
            return Response(data={
                'error': 'У Вас нет доступа к созданию заявок',
                'msg': 'Вы не являетесь проживающим в общежитии'
            }, status=status.HTTP_403_FORBIDDEN)
