from rest_framework import status
from rest_framework.response import Response
from .models import (
    Staff,
    Student,
    Resident
)
from .serializers import (
    StaffSerializer,
    StudentSerializer,
    ResidentSerializer,
    ResidentCreateSerializer
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

    def create(self, request, *args, **kwargs):
        serializer = self.create_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
