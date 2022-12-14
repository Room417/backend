from typing import Union

import pydantic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import F, CharField, functions, Value

from .models import (
    Staff,
    Student,
    Resident, Room
)
from .serializers import (
    StaffSerializer,
    StudentSerializer,
    ResidentSerializer,
    ResidentCreateSerializer,
    RelocateRoomResidentSchema,
)
from .mixins import DefaultViewMixin

from backend.permissions import StaffUserPermission


class StaffViewSet(DefaultViewMixin):
    """ ViewSet для взаимодействия с данными работников общежития """
    model = Staff
    serializer_class = StaffSerializer
    default_sort_fields = ['surname', 'name', 'patronymic']
    list_serializer = StaffSerializer
    detail_serializer = StaffSerializer
    permission_classes = [IsAuthenticated]

    def search_filter(self, filter_: str, include: list, order_by: list):
        return self.model.objects.prefetch_related(*include).annotate(
            temp=functions.Concat(
                F('surname'),
                Value(' '),
                F('name'),
                Value(' '),
                F('patronymic'),
                output_field=CharField(),
            )
        ).filter(temp__icontains=filter_).order_by(*order_by)

    @action(methods=['post'], detail=False, url_path='staff:search')
    def search(self, request, *args, **kwargs):
        return super().search(request, *args, **kwargs)

    @action(methods=['post'], detail=False, url_path='staff:search-one')
    def search_one(self, request, *args, **kwargs):
        return super().search_one(request, *args, **kwargs)


class StudentViewSet(DefaultViewMixin):
    """ ViewSet для взаимодействия с данными студентов """
    model = Student
    serializer_class = StudentSerializer
    list_serializer = StudentSerializer
    detail_serializer = StudentSerializer
    default_sort_fields = ['surname', 'name', 'patronymic']
    permission_classes = [StaffUserPermission]

    @action(methods=['post'], detail=False, url_path='students:search')
    def search(self, request, *args, **kwargs):
        return super().search(request, *args, **kwargs)

    @action(methods=['post'], detail=False, url_path='students:search-one')
    def search_one(self, request, *args, **kwargs):
        return super().search_one(request, *args, **kwargs)


class ResidentsViewSet(DefaultViewMixin):
    """ ViewSet для взаимодействия с данными проживающих общежития """
    model = Resident
    serializer_class = ResidentSerializer
    list_serializer = ResidentSerializer
    detail_serializer = ResidentSerializer
    default_sort_fields = ['student__surname', 'student__name', 'student__patronymic']
    create_serializer = ResidentCreateSerializer
    permission_classes = [StaffUserPermission]

    def search_filter(self, filter_: str, include: list, order_by: list):
        return self.model.objects.prefetch_related(*include).annotate(
            temp=functions.Concat(
                F('student__surname'),
                Value(' '),
                F('student__name'),
                Value(' '),
                F('student__patronymic'),
                Value(' '),
                functions.Cast(F('student__student_card'), output_field=CharField()),
                output_field=CharField(),
            )
        ).filter(temp__icontains=filter_).order_by(*order_by)

    def _get_object(self, model: Union[Room, Resident], **kwargs) -> Union[Room, Resident, dict]:
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return {
                'error': 'Объект не найден',
                'msg': '{model} с таким id не существует'
            }

    def create(self, request, *args, **kwargs):
        serializer = self.create_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['post'], detail=False, url_path='residents:relocate')
    def relocate(self, request, *args, **kwargs):
        try:
            schema = RelocateRoomResidentSchema(**self.request.data)
        except pydantic.error_wrappers.ValidationError as ex:
            return Response(data={
                'error': 'Переданы некорректные поля, проверьте тело запроса.',
                'msg': ex.errors()
            }, status=status.HTTP_400_BAD_REQUEST)
        room = self._get_object(number=schema.room_num, model=Room, building__number=schema.building_num)
        resident = self._get_object(student__student_card=schema.student_card, model=Resident)
        if isinstance(room, dict):
            room['msg'] = room['msg'].format(model='Комнаты')
            return Response(data=room, status=status.HTTP_400_BAD_REQUEST)
        if isinstance(resident, dict):
            resident['msg'] = resident['msg'].format(model='Проживающего')
            return Response(data=resident, status=status.HTTP_400_BAD_REQUEST)

        if room.is_full:
            return Response(data={
                'error': 'Переселение невозможно',
                'msg': 'Комната заполнена. Переселение невозможно'
            }, status=status.HTTP_400_BAD_REQUEST)

        resident.room = room
        resident.save(update_fields=['room'])

        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='residents:search')
    def search(self, request, *args, **kwargs):
        return super().search(request, *args, **kwargs)

    @action(methods=['post'], detail=False, url_path='residents:search-one')
    def search_one(self, request, *args, **kwargs):
        return super().search_one(request, *args, **kwargs)
