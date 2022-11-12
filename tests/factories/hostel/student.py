import pytest
import factory

from hostel_api.models import Student


@pytest.fixture
def student_factory():
    class StudentFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = Student

        surname = factory.Sequence(lambda i: f'surname{i}')
        name = factory.Sequence(lambda i: f'name{i}')
        patronymic = factory.Sequence(lambda i: f'patronymic{i}')
        group = factory.Sequence(lambda i: f'group{i}')
        study_direction = factory.Sequence(lambda i: f'study_direction{i}')
        student_card = factory.Sequence(lambda i: i)

    return StudentFactory
