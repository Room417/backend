from typing import Union

import pydantic
from rest_framework import status
from rest_framework.response import Response
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


class StaffViewSet(DefaultViewMixin):
    """ ViewSet для взаимодействия с данными работников общежития """
    model = Staff
    serializer_class = StaffSerializer
    default_sort_fields = ['surname', 'name', 'patronymic']


class StudentViewSet(DefaultViewMixin):
    """ ViewSet для взаимодействия с данными студентов """
    model = Student
    serializer_class = StudentSerializer
    default_sort_fields = ['surname', 'name', 'patronymic']


class ResidentsViewSet(DefaultViewMixin):
    """ ViewSet для взаимодействия с данными проживающих общежития """
    model = Resident
    serializer_class = ResidentSerializer
    default_sort_fields = ['student__surname', 'student__name', 'student__patronymic']
    create_serializer = ResidentCreateSerializer

    def _get_object(self, id_: int, model: Union[Room, Resident]) -> Union[Room, Resident, dict]:
        try:
            return model.objects.get(id=id_)
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

    def relocate(self, request, *args, **kwargs):
        try:
            schema = RelocateRoomResidentSchema(**self.request.data)
        except pydantic.error_wrappers.ValidationError as ex:
            return Response(data={
                'error': 'Переданы некорректные поля, проверьте тело запроса.',
                'msg': ex.errors()
            }, status=status.HTTP_400_BAD_REQUEST)
        room = self._get_object(id_=schema.room_id, model=Room)
        resident = self._get_object(id_=schema.resident_id, model=Resident)
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
